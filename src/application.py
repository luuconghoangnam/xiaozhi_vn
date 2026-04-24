import asyncio
import sys
import threading
import unicodedata
from pathlib import Path
from typing import Any, Awaitable

# 允许作为脚本直接运行：把项目根目录加入 sys.path（src 的上一级）
try:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
except Exception:
    pass

from src.constants.constants import DeviceState, ListeningMode
from src.plugins.calendar import CalendarPlugin
from src.plugins.iot import IoTPlugin
from src.plugins.manager import PluginManager
from src.plugins.mcp import McpPlugin
from src.plugins.shortcuts import ShortcutsPlugin
from src.plugins.status_beep import StatusBeepPlugin
from src.plugins.ui import UIPlugin
from src.plugins.wake_word import WakeWordPlugin
from src.protocols.mqtt_protocol import MqttProtocol
from src.protocols.websocket_protocol import WebsocketProtocol
from src.utils.config_manager import ConfigManager
from src.utils.logging_config import get_logger
from src.utils.opus_loader import setup_opus

logger = get_logger(__name__)
setup_opus()


class Application:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = Application()
        return cls._instance

    def __init__(self):
        if Application._instance is not None:
            logger.error("尝试创建Application的多个实例")
            raise Exception("Application是单例类，请使用get_instance()获取实例")
        Application._instance = self

        logger.debug("初始化Application实例")

        # 配置
        self.config = ConfigManager.get_instance()

        # 状态
        self.running = False
        self.protocol = None

        # 设备状态（仅主程序改写，插件只读）
        self.device_state = DeviceState.IDLE
        try:
            aec_enabled_cfg = bool(self.config.get_config("AEC_OPTIONS.ENABLED", True))
        except Exception:
            aec_enabled_cfg = True
        self.aec_enabled = aec_enabled_cfg
        self.listening_mode = (
            ListeningMode.REALTIME if self.aec_enabled else ListeningMode.AUTO_STOP
        )
        self.keep_listening = False
        self.aborted = False
        self._suppress_current_tts_audio = False

        # 统一任务池（替代 _main_tasks/_bg_tasks）
        self._tasks: set[asyncio.Task] = set()

        # 关停事件
        self._shutdown_event: asyncio.Event | None = None

        # 事件循环
        self._main_loop: asyncio.AbstractEventLoop | None = None

        # 并发控制
        self._state_lock: asyncio.Lock | None = None
        self._connect_lock: asyncio.Lock | None = None

        # 插件
        self.plugins = PluginManager()

        self.status_details = {
            'status': 'Đang khởi động...',
            'task': '',
            'response': '',
            'meta': '',
        }

    # -------------------------
    # 生命周期
    # -------------------------
    async def run(self, *, protocol: str = "websocket", mode: str = "gui") -> int:
        logger.info("启动Application，protocol=%s", protocol)
        try:
            self.running = True
            self._main_loop = asyncio.get_running_loop()
            self._initialize_async_objects()
            self._set_protocol(protocol)
            self._setup_protocol_callbacks()
            # 插件：setup（延迟导入AudioPlugin，确保上面setup_opus已执行）
            from src.plugins.audio import AudioPlugin

            # 注册音频、UI、MCP、IoT、唤醒词、快捷键与日程插件（UI模式从run参数传入）
            # 插件会自动按 priority 排序：
            # AudioPlugin(10) -> McpPlugin(20) -> WakeWordPlugin(30) -> CalendarPlugin(40)
            # -> IoTPlugin(50) -> UIPlugin(60) -> ShortcutsPlugin(70)
            self.plugins.register(
                McpPlugin(),
                IoTPlugin(),
                AudioPlugin(),
                WakeWordPlugin(),
                CalendarPlugin(),
                StatusBeepPlugin(),
                UIPlugin(mode=mode),
                ShortcutsPlugin(),
            )
            await self.plugins.setup_all(self)
            # 启动后广播初始状态，确保 UI 就绪时能看到“待命”
            try:
                await self.plugins.notify_device_state_changed(self.device_state)
            except Exception:
                pass
            # Auto-connect on startup so device shows online in web UI
            await self.connect_protocol()

            # Default production behavior: stay ready in background and wait for wake word.
            # Set XIAOZHI_AUTOSTART_LISTEN=1 only when explicitly testing bypass mode.
            try:
                import os
                if os.getenv('XIAOZHI_AUTOSTART_LISTEN', '0') == '1':
                    await self.start_auto_conversation()
            except Exception:
                pass
            # 插件：start
            await self.plugins.start_all()
            # 等待关停
            await self._wait_shutdown()
            return 0

        except Exception as e:
            logger.error(f"应用运行失败: {e}", exc_info=True)
            return 1
        finally:
            try:
                await self.shutdown()
            except Exception as e:
                logger.error(f"关闭应用时出错: {e}")

    async def connect_protocol(self):
        """
        确保协议通道打开并广播一次协议就绪。返回是否已打开。
        """
        # 已打开直接返回
        try:
            if self.is_audio_channel_opened():
                return True
            if not self._connect_lock:
                # 未初始化锁时，直接尝试一次
                opened = await asyncio.wait_for(
                    self.protocol.open_audio_channel(), timeout=12.0
                )
                if not opened:
                    logger.error("协议连接失败")
                    return False
                logger.info("协议连接已建立，按Ctrl+C退出")
                await self.plugins.notify_protocol_connected(self.protocol)
                return True

            async with self._connect_lock:
                if self.is_audio_channel_opened():
                    return True
                opened = await asyncio.wait_for(
                    self.protocol.open_audio_channel(), timeout=12.0
                )
                if not opened:
                    logger.error("协议连接失败")
                    return False
                logger.info("协议连接已建立，按Ctrl+C退出")
                await self.plugins.notify_protocol_connected(self.protocol)
                return True
        except asyncio.TimeoutError:
            logger.error("协议连接超时")
            return False

    def _initialize_async_objects(self) -> None:
        logger.debug("初始化异步对象")
        self._shutdown_event = asyncio.Event()
        self._state_lock = asyncio.Lock()
        self._connect_lock = asyncio.Lock()

    def _set_protocol(self, protocol_type: str) -> None:
        logger.debug("设置协议类型: %s", protocol_type)
        if protocol_type == "mqtt":
            self.protocol = MqttProtocol(asyncio.get_running_loop())
        else:
            self.protocol = WebsocketProtocol()

    # -------------------------
    # 手动聆听（按住说话）
    # -------------------------
    async def start_listening_manual(self) -> None:
        try:
            ok = await self.connect_protocol()
            if not ok:
                return
            self.keep_listening = False

            # 如果说话中发送打断
            if self.device_state == DeviceState.SPEAKING:
                logger.info("说话中发送打断")
                await self.protocol.send_abort_speaking(None)
                await self.set_device_state(DeviceState.IDLE)
            await self.protocol.send_start_listening(ListeningMode.MANUAL)
            await self.set_device_state(DeviceState.LISTENING)
        except Exception:
            pass

    async def stop_listening_manual(self) -> None:
        try:
            await self.protocol.send_stop_listening()
            await self.set_device_state(DeviceState.IDLE)
        except Exception:
            pass

    # -------------------------
    # 自动/实时对话：根据 AEC 与当前配置选择模式，开启保持会话
    # -------------------------
    async def start_auto_conversation(self) -> None:
        try:
            # Clear aborted flag when starting a new auto conversation
            self.aborted = False
            
            # Reset state if already in an active session to ensure clean start
            if self.device_state != DeviceState.IDLE:
                await self.set_device_state(DeviceState.IDLE)
                await asyncio.sleep(0.1)

            ok = await self.connect_protocol()
            if not ok:
                logger.error("Không thể kết nối đến server để bắt đầu hội thoại.")
                return

            mode = (
                ListeningMode.REALTIME if self.aec_enabled else ListeningMode.AUTO_STOP
            )
            self.listening_mode = mode
            self.keep_listening = True
            await self.protocol.send_start_listening(mode)
            await self.set_device_state(DeviceState.LISTENING)
        except Exception as e:
            logger.error(f"Khởi động đối thoại tự động thất bại: {e}")
            pass

    def _setup_protocol_callbacks(self) -> None:
        self.protocol.on_network_error(self._on_network_error)
        self.protocol.on_incoming_json(self._on_incoming_json)
        self.protocol.on_incoming_audio(self._on_incoming_audio)
        self.protocol.on_audio_channel_opened(self._on_audio_channel_opened)
        self.protocol.on_audio_channel_closed(self._on_audio_channel_closed)

    async def _wait_shutdown(self) -> None:
        await self._shutdown_event.wait()

    # -------------------------
    # 统一任务管理（精简）
    # -------------------------
    def spawn(self, coro: Awaitable[Any], name: str) -> asyncio.Task:
        """
        创建任务并登记，关停时统一取消。
        """
        if not self.running or (self._shutdown_event and self._shutdown_event.is_set()):
            logger.debug(f"跳过任务创建（应用正在关闭）: {name}")
            return None
        task = asyncio.create_task(coro, name=name)
        self._tasks.add(task)

        def _done(t: asyncio.Task):
            self._tasks.discard(t)
            if not t.cancelled() and t.exception():
                logger.error(f"任务 {name} 异常结束: {t.exception()}", exc_info=True)

        task.add_done_callback(_done)
        return task

    def schedule_command_nowait(self, fn, *args, **kwargs) -> None:
        if not self._main_loop or self._main_loop.is_closed():
            logger.warning("主事件循环未就绪，拒绝调度")
            return

        def _runner():
            try:
                res = fn(*args, **kwargs)
                if asyncio.iscoroutine(res):
                    self.spawn(res, name=f"call:{getattr(fn, '__name__', 'anon')}")
            except Exception as e:
                logger.error(f"调度的可调用执行失败: {e}", exc_info=True)

        # 确保在事件循环线程里执行
        self._main_loop.call_soon_threadsafe(_runner)

    # -------------------------
    # 协议回调
    # -------------------------
    def _on_network_error(self, error_message=None):
        if error_message:
            logger.error(error_message)

        # If we were in auto mode (keep_listening=True), try to reconnect
        if self.keep_listening:
            logger.info("Phát hiện lỗi mạng, đang thử kết nối lại...")
            # Use spawn to avoid blocking the network callback
            self.spawn(self.start_auto_conversation(), "state:reconnect_auto")
        else:
            self.keep_listening = False
        # 出错即请求关闭
        # if self._shutdown_event and not self._shutdown_event.is_set():
        #     self._shutdown_event.set()

    def _on_incoming_audio(self, data: bytes):
        logger.debug(f"收到二进制消息，长度: {len(data)}")
        # 转发给插件
        self.spawn(self.plugins.notify_incoming_audio(data), "plugin:on_audio")

    def _on_incoming_json(self, json_data):
        try:
            msg_type = json_data.get("type") if isinstance(json_data, dict) else None
            logger.info(f"收到JSON消息: type={msg_type}")
            # 将 TTS start/stop 映射为设备状态（支持自动/实时，且不污染手动模式）
            if msg_type == "tts":
                state = json_data.get("state")
                
                # Auto-pause all music players while TTS is speaking
                try:
                    from src.mcp.tools.youtube.youtube_player import get_youtube_player_instance
                    from src.mcp.tools.music.music_player import get_music_player_instance
                    yt_player = get_youtube_player_instance()
                    music_player = get_music_player_instance()
                except Exception:
                    yt_player = None
                    music_player = None

                if state == "start":
                    text = json_data.get("text", "")
                    normalized_text = text.lower()

                    def _norm_no_accents(s: str) -> str:
                        s = (s or "").lower().strip()
                        s = unicodedata.normalize("NFD", s)
                        s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
                        return " ".join(s.split())

                    normalized_text_ascii = _norm_no_accents(text)

                    goodbye_keywords = [
                        "chắc anh đang bận",
                        "hẹn gặp lại",
                        "tạm biệt anh",
                        "tạm biệt",
                    ]
                    greeting_keywords = [
                        "xin chào",
                        "chào anh",
                        "em chào",
                        "rất vui được gặp",
                    ]
                    is_server_goodbye = any(
                        kw in normalized_text for kw in goodbye_keywords
                    )
                    is_duplicate_greeting = (
                        self.device_state in (DeviceState.SPEAKING, DeviceState.LISTENING)
                        and any(kw in normalized_text for kw in greeting_keywords)
                    )

                    idle_notice_keywords_ascii = [
                        "san sang",
                        "cho wake word",
                        "cho tu danh thuc",
                        "khi nao anh can",
                        "em se cho",
                        "khong co lenh",
                        "khong hoat dong",
                        "het thoi gian",
                        "timeout",
                    ]
                    is_idle_notice = (
                        self.device_state == DeviceState.LISTENING
                        and any(kw in normalized_text_ascii for kw in idle_notice_keywords_ascii)
                    )

                    if is_idle_notice:
                        logger.info(
                            f"Suppressing server idle/ready TTS; beep only. text='{text}'"
                        )
                        self._suppress_current_tts_audio = True

                        async def _clear_suppress_later():
                            try:
                                await asyncio.sleep(2.0)
                                self._suppress_current_tts_audio = False
                            except Exception:
                                pass

                        self.spawn(_clear_suppress_later(), "tts:clear_suppress_idle_notice")
                        try:
                            from src.constants.constants import AbortReason

                            self.spawn(
                                self.protocol.send_abort_speaking(AbortReason.NONE),
                                "tts:abort_idle_notice",
                            )
                        except Exception:
                            pass
                        self.keep_listening = False
                        self.spawn(
                            self.set_device_state(DeviceState.IDLE),
                            "state:idle_notice_idle",
                        )
                        return

                    if is_server_goodbye or is_duplicate_greeting:
                        logger.info(
                            f"Bỏ qua TTS phụ từ server: '{text}'. Ưu tiên luồng giao tiếp hiện tại."
                        )
                        self._suppress_current_tts_audio = True
                        if is_server_goodbye:
                            self.keep_listening = False
                            self.spawn(self.set_device_state(DeviceState.IDLE), "state:goodbye_idle")
                        return

                    self._suppress_current_tts_audio = False

                    if yt_player and yt_player.is_playing:
                        self.spawn(yt_player.pause(), "plugin:pause_youtube_for_tts")
                    if music_player and music_player.is_playing:
                        self.spawn(music_player.pause(source="tts"), "plugin:pause_music_for_tts")
                        
                    # 仅当保持会话且实时模式时，TTS开始期间保持LISTENING；否则显示SPEAKING
                    if (
                        self.keep_listening
                        and self.listening_mode == ListeningMode.REALTIME
                    ):
                        self.spawn(
                            self.set_device_state(DeviceState.LISTENING),
                            "state:tts_start_rt",
                        )
                    else:
                        self.spawn(
                            self.set_device_state(DeviceState.SPEAKING),
                            "state:tts_start_speaking",
                        )
                elif state == "stop":
                    self._suppress_current_tts_audio = False
                    if yt_player and yt_player.is_playing and yt_player.paused:
                        self.spawn(yt_player.resume(), "plugin:resume_youtube_after_tts")

                    if (
                        self.keep_listening
                        and self.listening_mode == ListeningMode.REALTIME
                    ):
                        # 继续对话：根据当前模式重启监听
                        async def _restart_listening():
                            try:
                                # 先设置状态为 LISTENING，触发音频队列清空和硬件停止等待
                                await self.set_device_state(DeviceState.LISTENING)

                                # Always send start_listening to ensure server VAD is active
                                await self.protocol.send_start_listening(
                                    self.listening_mode
                                )
                            except Exception:
                                pass

                        self.spawn(_restart_listening(), "state:tts_stop_restart")
                    else:
                        self.keep_listening = False
                        self.spawn(
                            self.set_device_state(DeviceState.IDLE),
                            "state:tts_stop_idle",
                        )
            elif msg_type == "goodbye":
                logger.info("Nhận goodbye từ server, về IDLE và dừng auto-listen.")
                self.keep_listening = False
                self._suppress_current_tts_audio = False
                self.spawn(self.set_device_state(DeviceState.IDLE), "state:goodbye_idle")
            # 转发给插件
            self.spawn(self.plugins.notify_incoming_json(json_data), "plugin:on_json")
        except Exception:
            logger.info("收到JSON消息")

    async def _on_audio_channel_opened(self):
        logger.info("协议通道已打开")
        # 通道打开后进入 LISTENING（：简化为直读直写）
        # Audio channel opened => ready. Stay IDLE until wake word/manual start listening.
        await self.set_device_state(DeviceState.IDLE)

    async def _on_audio_channel_closed(self):
        logger.info("协议通道已关闭")
        # Dừng hẳn chế độ tự động nghe khi kênh bị đóng (tránh lặp vô hạn)
        self.keep_listening = False
        await self.set_device_state(DeviceState.IDLE)
        logger.info("Đã về trạng thái IDLE, chờ Wake Word hoặc kích hoạt thủ công.")

    async def set_device_state(self, state: DeviceState):
        """
        仅供主程序内部调用：设置设备状态。插件请只读获取。
        """
        # print(f"set_device_state: {state}")
        if not self._state_lock:
            self.device_state = state
            try:
                await self.plugins.notify_device_state_changed(state)
            except Exception:
                pass
            return
        async with self._state_lock:
            if self.device_state == state:
                return
            logger.info(f"设置设备状态: {state}")
            self.device_state = state
        # 锁外广播，避免插件回调引起潜在的长耗时阻塞
        try:
            await self.plugins.notify_device_state_changed(state)
            if state == DeviceState.LISTENING:
                self.aborted = False
        except Exception:
            pass

    # -------------------------
    # 只读访问器（提供给插件使用）
    # -------------------------
    def get_device_state(self):
        return self.device_state

    def is_idle(self) -> bool:
        return self.device_state == DeviceState.IDLE

    def is_listening(self) -> bool:
        return self.device_state == DeviceState.LISTENING

    def is_speaking(self) -> bool:
        return self.device_state == DeviceState.SPEAKING

    def get_listening_mode(self):
        return self.listening_mode

    def is_keep_listening(self) -> bool:
        return bool(self.keep_listening)

    def is_audio_channel_opened(self) -> bool:
        try:
            return bool(self.protocol and self.protocol.is_audio_channel_opened())
        except Exception:
            return False

    def should_capture_audio(self) -> bool:
        try:
            if self.device_state == DeviceState.LISTENING and not self.aborted:
                return True

            return (
                self.device_state == DeviceState.SPEAKING
                and self.aec_enabled
                and self.keep_listening
                and self.listening_mode == ListeningMode.REALTIME
            )
        except Exception:
            return False

    def should_play_incoming_audio(self) -> bool:
        return not bool(getattr(self, "_suppress_current_tts_audio", False))

    def get_state_snapshot(self) -> dict:
        return {
            "device_state": self.device_state,
            "listening_mode": self.listening_mode,
            "keep_listening": bool(self.keep_listening),
            "audio_opened": self.is_audio_channel_opened(),
        }

    async def abort_speaking(self, reason):
        """
        中止语音输出.
        """

        if self.aborted:
            logger.debug(f"已经中止，忽略重复的中止请求: {reason}")
            return

        logger.info(f"中止语音输出，原因: {reason}")
        self.aborted = True
        await self.protocol.send_abort_speaking(reason)
        await self.set_device_state(DeviceState.IDLE)

    # -------------------------
    # UI 辅助：供插件或工具直接调用
    # -------------------------
    def set_chat_message(self, role, message: str) -> None:
        """将文本更新转发为 UI 可识别的 JSON 消息（复用 UIPlugin 的 on_incoming_json）。
        role: "assistant" | "user" 影响消息类型映射。
        """
        try:
            msg_type = "tts" if str(role).lower() == "assistant" else "stt"
        except Exception:
            msg_type = "tts"
        payload = {"type": msg_type, "text": message}
        # 通过插件事件总线异步派发
        self.spawn(self.plugins.notify_incoming_json(payload), "ui:text_update")

    def set_status_details(self, **kwargs) -> None:
        try:
            for key, value in kwargs.items():
                if key in self.status_details and value is not None:
                    self.status_details[key] = str(value)

            payload = {
                "type": "status_details",
                "status": self.status_details.get("status", ""),
                "task": self.status_details.get("task", ""),
                "response": self.status_details.get("response", ""),
                "meta": self.status_details.get("meta", ""),
            }
            self.spawn(self.plugins.notify_incoming_json(payload), "ui:status_details_update")
        except Exception:
            pass

    def set_emotion(self, emotion: str) -> None:
        """
        设置情绪表情：通过 UIPlugin 的 on_incoming_json 路由。
        """
        payload = {"type": "llm", "emotion": emotion}
        self.spawn(self.plugins.notify_incoming_json(payload), "ui:emotion_update")

    # -------------------------
    # 关停
    # -------------------------
    async def shutdown(self):
        if not self.running:
            return
        logger.info("正在关闭Application...")
        self.running = False

        if self._shutdown_event is not None:
            self._shutdown_event.set()

        try:
            # 取消所有登记任务
            if self._tasks:
                for t in list(self._tasks):
                    if not t.done():
                        t.cancel()
                await asyncio.gather(*self._tasks, return_exceptions=True)
                self._tasks.clear()

            # 关闭协议（限时，避免阻塞退出）
            if self.protocol:
                try:
                    try:
                        self._main_loop.create_task(self.protocol.close_audio_channel())
                    except asyncio.TimeoutError:
                        logger.warning("关闭协议超时，跳过等待")
                except Exception as e:
                    logger.error(f"关闭协议失败: {e}")

            # 插件：stop/shutdown
            try:
                await self.plugins.stop_all()
            except Exception:
                pass
            try:
                await self.plugins.shutdown_all()
            except Exception:
                pass

            logger.info("Application 关闭完成")
        except Exception as e:
            logger.error(f"关闭应用时出错: {e}", exc_info=True)
