import asyncio
import time
from pathlib import Path
from typing import Dict, List, Optional

from src.audio_codecs.music_decoder import MusicDecoder
from src.constants.constants import AudioConfig
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

class RadioStation:
    def __init__(self, name: str, url: str, description: str):
        self.name = name
        self.url = url
        self.description = description

class RadioPlayer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RadioPlayer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.decoder: Optional[MusicDecoder] = None
        self._radio_queue: Optional[asyncio.Queue] = None
        self._playback_task: Optional[asyncio.Task] = None
        self.is_playing = False
        self.current_station = ""
        
        self.stations = {
            "VOV1": RadioStation("VOV1 - Thời sự", "https://stream.vovmedia.vn/vov-1", "Tin tức & thời sự quốc gia"),
            "VOV2": RadioStation("VOV2 - Văn hóa & Giáo dục", "https://stream.vovmedia.vn/vov-2", "Văn hóa - giáo dục - xã hội"),
            "VOV3": RadioStation("VOV3 - Âm nhạc & Giải trí", "https://stream.vovmedia.vn/vov-3", "Nhạc & giải trí tổng hợp"),
            "VOV_GT_HN": RadioStation("VOV Giao thông Hà Nội", "https://stream.vovmedia.vn/vovgt-hn", "Giao thông & đời sống Hà Nội"),
            "VOV_GT_HCM": RadioStation("VOV Giao thông TP.HCM", "https://stream.vovmedia.vn/vovgt-hcm", "Giao thông & đời sống TP.HCM"),
            "VOV_MEKONG": RadioStation("VOV Mekong FM", "https://stream.vovmedia.vn/vovmekong", "Miền Tây - Đồng bằng sông Cửu Long"),
        }
        
        self.app = None
        self.audio_codec = None
        self._initialize_app_reference()
        self._initialized = True

    def _initialize_app_reference(self):
        try:
            from src.application import Application
            self.app = Application.get_instance()
            self.audio_codec = getattr(self.app, "audio_codec", None)
        except Exception as e:
            logger.warning(f"RadioPlayer: Failed to get Application instance: {e}")

    async def play_station(self, station_key: str) -> dict:
        if station_key not in self.stations:
            # Try fuzzy match
            found = None
            for k, s in self.stations.items():
                if station_key.lower() in s.name.lower() or station_key.lower() in k.lower():
                    found = k
                    break
            if not found:
                return {"status": "error", "message": f"Không tìm thấy đài: {station_key}"}
            station_key = found

        station = self.stations[station_key]
        logger.info(f"Đang phát Radio: {station.name} ({station.url})")

        await self.stop()

        self.is_playing = True
        self.current_station = station.name
        self._radio_queue = asyncio.Queue(maxsize=100)
        
        self.decoder = MusicDecoder(
            sample_rate=AudioConfig.OUTPUT_SAMPLE_RATE,
            channels=AudioConfig.CHANNELS,
        )

        # Radio streams don't have a file path, but MusicDecoder uses subprocess with URL
        # We need to make sure MusicDecoder can handle URLs
        success = await self.decoder.start_decode(Path(station.url), self._radio_queue)
        
        if success:
            self._playback_task = asyncio.create_task(self._playback_loop())
            return {"status": "success", "message": f"Đang phát: {station.name}"}
        else:
            self.is_playing = False
            return {"status": "error", "message": "Không thể kết nối đến luồng Radio"}

    async def _playback_loop(self):
        try:
            while self.is_playing:
                if self._radio_queue.empty():
                    await asyncio.sleep(0.01)
                    continue
                
                audio_frame = await self._radio_queue.get()
                if audio_frame is None: # EOF
                    break
                
                if self.audio_codec:
                    await self.audio_codec.put_audio_data(audio_frame)
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Radio playback loop error: {e}")
        finally:
            self.is_playing = False

    async def stop(self) -> dict:
        if not self.is_playing:
            return {"status": "info", "message": "Radio đang không phát"}

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
        
        return {"status": "success", "message": "Đã dừng Radio"}

    async def get_stations(self) -> dict:
        list_str = "\n".join([f"- {k}: {s.name} ({s.description})" for k, s in self.stations.items()])
        return {"status": "success", "message": f"Danh sách đài Radio Việt Nam:\n{list_str}"}

def get_radio_player_instance() -> RadioPlayer:
    return RadioPlayer()
