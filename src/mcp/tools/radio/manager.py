from typing import Any, Dict
from src.utils.logging_config import get_logger
from .radio_player import get_radio_player_instance

logger = get_logger(__name__)

class RadioToolsManager:
    def __init__(self):
        self._initialized = False
        self._radio_player = None

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        try:
            self._radio_player = get_radio_player_instance()
            
            # Register Play Radio
            self._register_play_radio_tool(add_tool, PropertyList, Property, PropertyType)
            
            # Register Stop Radio
            self._register_stop_radio_tool(add_tool, PropertyList)
            
            # Register List Stations
            self._register_list_stations_tool(add_tool, PropertyList)
            
            self._initialized = True
            logger.info("[RadioManager] Vietnamese Radio tools registered")
        except Exception as e:
            logger.error(f"[RadioManager] Registration failed: {e}")

    def _register_play_radio_tool(self, add_tool, PropertyList, Property, PropertyType):
        async def play_radio_wrapper(args: Dict[str, Any]) -> str:
            station = args.get("station", "VOV1")
            result = await self._radio_player.play_station(station)
            return result.get("message", "Đã thực hiện")

        props = PropertyList([Property("station", PropertyType.STRING, description="Tên đài hoặc mã đài (VD: VOV1, VOV3, Giao thông)")])
        add_tool(("radio.play", "Phát đài Radio Việt Nam (VOV). Hỗ trợ VOV1, VOV2, VOV3, VOV Giao thông, Mekong.", props, play_radio_wrapper))

    def _register_stop_radio_tool(self, add_tool, PropertyList):
        async def stop_radio_wrapper(args: Dict[str, Any]) -> str:
            result = await self._radio_player.stop()
            return result.get("message", "Đã dừng")

        add_tool(("radio.stop", "Dừng phát Radio.", PropertyList(), stop_radio_wrapper))

    def _register_list_stations_tool(self, add_tool, PropertyList):
        async def list_stations_wrapper(args: Dict[str, Any]) -> str:
            result = await self._radio_player.get_stations()
            return result.get("message", "Danh sách đài")

        add_tool(("radio.list_stations", "Liệt kê danh sách các đài Radio Việt Nam có sẵn.", PropertyList(), list_stations_wrapper))

_radio_tools_manager = None

def get_radio_tools_manager() -> RadioToolsManager:
    global _radio_tools_manager
    if _radio_tools_manager is None:
        _radio_tools_manager = RadioToolsManager()
    return _radio_tools_manager
