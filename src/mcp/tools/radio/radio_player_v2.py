import asyncio
from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np

from src.audio_codecs.music_decoder import MusicDecoder
from src.constants.constants import AudioConfig
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class RadioStation:
    name: str
    url: str
    description: str


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

        self._deferred_station: Optional[str] = None

        # VOV streams (official)
        self.stations: Dict[str, RadioStation] = {
            "VOV1": RadioStation(
                "VOV1",
                "https://stream.vovmedia.vn/vov-1",
                "News / current affairs",
            ),
            "VOV2": RadioStation(
                "VOV2",
                "https://stream.vovmedia.vn/vov-2",
                "Culture / education",
            ),
            "VOV3": RadioStation(
                "VOV3",
                "https://stream.vovmedia.vn/vov-3",
                "Music / entertainment",
            ),
            "VOV_GT_HN": RadioStation(
                "VOV Traffic Hanoi",
                "https://stream.vovmedia.vn/vovgt-hn",
                "Traffic / Hanoi",
            ),
            "VOV_GT_HCM": RadioStation(
                "VOV Traffic HCM",
                "https://stream.vovmedia.vn/vovgt-hcm",
                "Traffic / HCM",
            ),
            "VOV_MEKONG": RadioStation(
                "VOV Mekong",
                "https://stream.vovmedia.vn/vovmekong",
                "Mekong Delta",
            ),
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

    def _should_defer_for_tts(self) -> bool:
        try:
            if self.app and hasattr(self.app, "is_speaking") and self.app.is_speaking():
                return True
            if self.audio_codec and self.audio_codec.get_audio_focus() == "tts":
                return True
        except Exception:
            pass
        return False

    async def play_deferred_if_ready(self) -> bool:
        station_key = self._deferred_station
        if not station_key or self._should_defer_for_tts():
            return False
        self._deferred_station = None
        result = await self.play_station(station_key)
        return result.get("status") == "success"

    async def play_station(self, station_key: str) -> dict:
        self._initialize_app_reference()

        # Resolve station key (exact -> fuzzy)
        station_key_norm = (station_key or "").strip()
        if not station_key_norm:
            station_key_norm = "VOV1"

        if station_key_norm not in self.stations:
            found = None
            for key, station in self.stations.items():
                if station_key_norm.lower() in key.lower() or station_key_norm.lower() in station.name.lower():
                    found = key
                    break
            if not found:
                return {"status": "error", "message": f"Khong tim thay dai: {station_key_norm}"}
            station_key_norm = found

        if self._should_defer_for_tts():
            self._deferred_station = station_key_norm
            logger.info("TTS is active, deferring radio playback until speech finishes")
            return {
                "status": "success",
                "message": "Da nhan lenh mo radio, se phat sau khi noi xong",
            }

        station = self.stations[station_key_norm]
        logger.info(f"Playing radio: {station.name} ({station.url})")

        await self.stop()

        self.is_playing = True
        self.current_station = station.name
        self._radio_queue = asyncio.Queue(maxsize=100)

        self.decoder = MusicDecoder(
            sample_rate=AudioConfig.OUTPUT_SAMPLE_RATE,
            channels=AudioConfig.CHANNELS,
        )

        # Pass URL as a plain string to avoid Windows Path mangling.
        success = await self.decoder.start_decode(station.url, self._radio_queue)
        if not success:
            self.is_playing = False
            return {"status": "error", "message": "Khong the ket noi den luong radio"}

        self._playback_task = asyncio.create_task(self._playback_loop())
        return {"status": "success", "message": f"Dang phat: {station.name}"}

    async def _playback_loop(self):
        try:
            while self.is_playing:
                if not self._radio_queue or self._radio_queue.empty():
                    await asyncio.sleep(0.01)
                    continue

                audio_frame = await self._radio_queue.get()
                if audio_frame is None:  # EOF
                    break

                if not self.audio_codec:
                    continue

                # Ensure mono int16.
                if isinstance(audio_frame, np.ndarray):
                    frame = audio_frame
                else:
                    frame = np.asarray(audio_frame, dtype=np.int16)

                if frame.ndim > 1:
                    frame = frame.mean(axis=1).astype(np.int16)

                await self.audio_codec.write_pcm_direct(frame, source="music")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Radio playback loop error: {e}", exc_info=True)
        finally:
            self.is_playing = False
            if self.audio_codec:
                try:
                    await self.audio_codec.release_audio_focus("music")
                except Exception:
                    pass

    async def stop(self) -> dict:
        if not self.is_playing:
            return {"status": "info", "message": "Radio dang khong phat"}

        self.is_playing = False

        if self.decoder:
            try:
                await self.decoder.stop()
            finally:
                self.decoder = None

        if self._playback_task:
            self._playback_task.cancel()
            try:
                await self._playback_task
            except asyncio.CancelledError:
                pass
            finally:
                self._playback_task = None

        if self.audio_codec:
            try:
                await self.audio_codec.release_audio_focus("music")
            except Exception:
                pass

        return {"status": "success", "message": "Da dung radio"}

    async def get_stations(self) -> dict:
        lines = []
        for key, station in self.stations.items():
            lines.append(f"- {key}: {station.name} ({station.description})")
        return {"status": "success", "message": "Danh sach dai:\n" + "\n".join(lines)}


def get_radio_player_instance() -> RadioPlayer:
    return RadioPlayer()

