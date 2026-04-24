import asyncio
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import yt_dlp

from src.audio_codecs.music_decoder import MusicDecoder
from src.constants.constants import AudioConfig
from src.utils.logging_config import get_logger
from src.utils.resource_finder import get_user_cache_dir, get_user_data_dir

logger = get_logger(__name__)

class YoutubePlayer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(YoutubePlayer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.decoder: Optional[MusicDecoder] = None
        self._audio_queue: Optional[asyncio.Queue] = None
        self._playback_task: Optional[asyncio.Task] = None
        self.is_playing = False
        self.paused = False
        self.current_title = ""
        self.current_url = ""
        
        # Cache directory
        user_data_dir = get_user_data_dir(create=True)
        self.cache_dir = user_data_dir / 'cache' / 'youtube'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.app = None
        self.audio_codec = None
        self._deferred_query: Optional[str] = None
        self._initialize_app_reference()
        self._initialized = True

    def _initialize_app_reference(self):
        try:
            from src.application import Application
            self.app = Application.get_instance()
            self.audio_codec = getattr(self.app, "audio_codec", None)
        except Exception as e:
            logger.warning(f"YoutubePlayer: Failed to get Application instance: {e}")

    def _should_defer_for_tts(self) -> bool:
        try:
            if self.app and hasattr(self.app, "is_speaking") and self.app.is_speaking():
                return True
            if self.audio_codec and self.audio_codec.get_audio_focus() == "tts":
                return True
        except Exception:
            pass
        return False

    def _extract_audio_url(self, video: dict) -> str:
        url = (
            video.get("url")
            or video.get("webpage_url")
            or video.get("original_url")
        )
        if url:
            return url

        formats = video.get("formats") or []
        audio_formats = [
            fmt
            for fmt in formats
            if fmt.get("url") and fmt.get("acodec") != "none"
        ]
        if audio_formats:
            return audio_formats[-1]["url"]

        raise ValueError("yt-dlp khong tra ve URL audio kha dung")

    async def play_deferred_if_ready(self) -> bool:
        query = self._deferred_query
        if not query or self._should_defer_for_tts():
            return False

        self._deferred_query = None
        result = await self.search_and_play(query)
        return result.get("status") == "success"

    async def search_and_play(self, query: str) -> dict:
        logger.info(f"YouTube searching for: {query}")
        
        # Stop current playback if any
        await self.stop()
        self._initialize_app_reference()

        if self._should_defer_for_tts():
            self._deferred_query = query
            logger.info("TTS is active, deferring YouTube playback until speech finishes")
            return {
                "status": "success",
                "message": "Da nhan lenh phat YouTube, se phat sau khi noi xong",
            }
        
        # Search using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await asyncio.to_thread(ydl.extract_info, f"ytsearch1:{query}", download=False)
                if not info or 'entries' not in info or not info['entries']:
                    logger.warning(f"Không tìm thấy bài hát trên YouTube: {query}")
                    return {"status": "error", "message": f"Không tìm thấy kết quả nào trên YouTube cho: {query}"}
                
                # Prefer actual videos (avoid channels/playlists when possible)
                entries = info.get("entries") or []
                video = None
                for e in entries:
                    try:
                        wurl = (e.get("webpage_url") or "").lower()
                        title = (e.get("title") or "").lower()
                        if "channel" in wurl or "/@" in wurl:
                            continue
                        if "playlist" in wurl:
                            continue
                        if "watch" in wurl or "youtu.be/" in wurl:
                            video = e
                            break
                        # Fallback: keep first non-empty entry
                        if video is None and (e.get("url") or e.get("webpage_url")):
                            video = e
                    except Exception:
                        continue
                if video is None:
                    video = entries[0]
                url = self._extract_audio_url(video)
                title = video.get('title', query)
                duration = video.get('duration', 0) or 0
                
                self.current_title = title
                self.current_url = url
                
                logger.info(f"Found YouTube video: {title} (Duration: {duration}s)")
                
                # Start playback
                self.is_playing = True
                self.paused = False
                self._audio_queue = asyncio.Queue(maxsize=100)
                
                self.decoder = MusicDecoder(
                    sample_rate=AudioConfig.OUTPUT_SAMPLE_RATE,
                    channels=AudioConfig.CHANNELS,
                )
                
                # Use the direct stream URL from yt-dlp (passed as string to avoid Windows path mangling)
                success = await self.decoder.start_decode(url, self._audio_queue)
                
                if success:
                    self._playback_task = asyncio.create_task(self._playback_loop())
                    return {
                        "status": "success", 
                        "message": f"Đang phát từ YouTube: {title}",
                        "title": title,
                        "duration": duration
                    }
                else:
                    self.is_playing = False
                    return {"status": "error", "message": "Không thể giải mã luồng âm thanh từ YouTube"}
                    
        except Exception as e:
            error_msg = str(e)
            logger.error(f"YouTube search/play error: {error_msg}")
            return {"status": "error", "message": f"Lỗi YouTube: {error_msg}"}

    async def _playback_loop(self):
        try:
            while self.is_playing:
                if self.paused:
                    # Keep draining to avoid the decoder queue filling up while paused.
                    try:
                        if self._audio_queue:
                            drained = 0
                            while drained < 50 and not self._audio_queue.empty():
                                try:
                                    _ = self._audio_queue.get_nowait()
                                    drained += 1
                                except asyncio.QueueEmpty:
                                    break
                    except Exception:
                        pass
                    await asyncio.sleep(0.05)
                    continue

                if self._audio_queue.empty():
                    await asyncio.sleep(0.01)
                    continue
                
                audio_frame = await self._audio_queue.get()
                if audio_frame is None: # EOF
                    break
                
                if self.audio_codec:
                    # Mono conversion if needed (MusicDecoder output is mono usually)
                    if audio_frame.ndim > 1:
                        audio_frame = audio_frame.mean(axis=1).astype(np.int16)
                    await self.audio_codec.write_pcm_direct(audio_frame, source="music")
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"YouTube playback loop error: {e}")
        finally:
            self.is_playing = False
            if self.audio_codec:
                await self.audio_codec.release_audio_focus("music")
            logger.info("YouTube playback finished")

    async def stop(self) -> dict:
        if not self.is_playing:
            return {"status": "info", "message": "YouTube đang không phát"}

        self.is_playing = False
        if self.decoder:
            await self.decoder.stop()
            self.decoder = None
        
        if self._playback_task:
            self._playback_task.cancel()
            try:
                await self._playback_task
            except asyncio.CancelledError:
                pass
        if self.audio_codec:
            await self.audio_codec.release_audio_focus("music")

        return {"status": "success", "message": "Đã dừng YouTube"}

    async def pause(self) -> dict:
        if not self.is_playing:
            return {"status": "info", "message": "YouTube đang không phát"}
        self.paused = True
        return {"status": "success", "message": "Đã tạm dừng YouTube"}

    async def resume(self) -> dict:
        if not self.is_playing:
            return {"status": "info", "message": "YouTube đang không phát"}
        self.paused = False
        return {"status": "success", "message": "Đã tiếp tục phát YouTube"}

def get_youtube_player_instance() -> YoutubePlayer:
    return YoutubePlayer()
