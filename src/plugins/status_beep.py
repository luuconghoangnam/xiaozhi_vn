from __future__ import annotations

import asyncio
import math
from typing import Any

import numpy as np

from src.constants.constants import AudioConfig, DeviceState
from src.plugins.base import Plugin
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class StatusBeepPlugin(Plugin):
    name = "status_beep"
    priority = 55  # after core audio/wakeword, before UI/shortcuts is fine

    def __init__(self) -> None:
        super().__init__()
        self.app = None
        self._last_state = None
        self._last_status_text = ""
        self._last_user_text = ""
        self._last_assistant_text = ""
        self._beep_lock = asyncio.Lock()

    async def setup(self, app: Any) -> None:
        self.app = app

    async def on_device_state_changed(self, state):
        try:
            state_str = str(state)
            self._last_state = state_str
            status_map = {
                DeviceState.IDLE: "Sẵn sàng chờ wake word",
                DeviceState.LISTENING: "Đang nghe anh nói...",
                DeviceState.SPEAKING: "Đang trả lời / thực hiện",
            }
            text = status_map.get(state_str, f"State: {state_str}")
            self._last_status_text = text
            if hasattr(self.app, "set_status_details"):
                self.app.set_status_details(status=text)

            # Beep when entering listening, and another beep when leaving listening back to idle
            prev = self._last_state
            # self._last_state already updated above, so use app.device_state snapshots via stored text logic
        except Exception:
            pass

        try:
            prev = getattr(self, "_prev_state_for_beep", None)
            self._prev_state_for_beep = state
            if state == DeviceState.LISTENING and prev != DeviceState.LISTENING:
                # Chơi bíp không chặn luồng chính để tránh lag
                asyncio.create_task(self._play_beep(pattern="listen_start"))
            elif prev == DeviceState.LISTENING and state == DeviceState.IDLE:
                asyncio.create_task(self._play_beep(pattern="listen_stop"))
        except Exception as e:
            logger.debug(f"beep state transition failed: {e}")

    async def on_incoming_json(self, message: Any) -> None:
        if not isinstance(message, dict):
            return
        try:
            msg_type = message.get("type")
            if msg_type == "stt":
                text = (message.get("text") or "").strip()
                if text:
                    self._last_user_text = text
                    if hasattr(self.app, "set_status_details"):
                        self.app.set_status_details(task=f"Nghe được: {text[:120]}")
            elif msg_type == "tts":
                state = message.get("state")
                text = (message.get("text") or "").strip()
                if text:
                    self._last_assistant_text = text
                    if hasattr(self.app, "set_status_details"):
                        self.app.set_status_details(response=f"Coonie: {text[:160]}")
                if state == "start" and hasattr(self.app, "set_status_details"):
                    self.app.set_status_details(status="Đang nói chuyện với anh...")
                elif state == "stop" and hasattr(self.app, "set_status_details"):
                    if getattr(self.app, "keep_listening", False):
                        self.app.set_status_details(status="Nói xong, quay lại chờ wake word / nghe tiếp")
                    else:
                        self.app.set_status_details(status="Nói xong, quay lại chờ wake word")
            elif msg_type == "llm":
                emotion = (message.get("emotion") or "").strip()
                if emotion and hasattr(self.app, "set_status_details"):
                    self.app.set_status_details(meta=f"Emotion: {emotion}")
        except Exception as e:
            logger.debug(f"status detail update failed: {e}")

    async def _play_beep(self, pattern: str = "listen_start") -> None:
        async with self._beep_lock:
            try:
                audio_plugin = self.app.plugins.get_plugin("audio") if self.app and hasattr(self.app, 'plugins') else None
                codec = getattr(audio_plugin, "codec", None) if audio_plugin else None
                if codec is None:
                    return

                if pattern == "listen_start":
                    tones = [(880, 0.08), (1320, 0.06)]
                else:
                    tones = [(660, 0.08)]

                pcm = self._build_tone_sequence(tones)
                await codec.write_pcm_direct(pcm, source="system")
                await codec.wait_output_drained(timeout=0.8)
                await codec.release_audio_focus("system")
            except Exception as e:
                logger.debug(f"play beep failed: {e}")

    def _build_tone_sequence(self, tones: list[tuple[int, float]]) -> np.ndarray:
        sr = AudioConfig.OUTPUT_SAMPLE_RATE
        chunks = []
        for freq, dur in tones:
            n = max(1, int(sr * dur))
            t = np.arange(n, dtype=np.float32) / float(sr)
            wave = 0.18 * np.sin(2.0 * math.pi * float(freq) * t)
            fade = max(1, int(sr * 0.008))
            env = np.ones(n, dtype=np.float32)
            f = min(fade, n // 2 if n >= 2 else 1)
            if f > 0:
                env[:f] = np.linspace(0.0, 1.0, f, dtype=np.float32)
                env[-f:] = np.linspace(1.0, 0.0, f, dtype=np.float32)
            wave *= env
            chunks.append(wave)
            gap = np.zeros(int(sr * 0.03), dtype=np.float32)
            chunks.append(gap)
        mono = np.concatenate(chunks) if chunks else np.zeros(AudioConfig.OUTPUT_FRAME_SIZE, dtype=np.float32)
        mono = np.clip(mono, -1.0, 1.0)
        pcm = (mono * 32767.0).astype(np.int16)
        return pcm
