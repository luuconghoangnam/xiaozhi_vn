from typing import Any, Dict
from src.utils.logging_config import get_logger
from .youtube_player import get_youtube_player_instance

logger = get_logger(__name__)

class YoutubeToolsManager:
    def __init__(self):
        self._initialized = False
        self._youtube_player = None

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        try:
            self._youtube_player = get_youtube_player_instance()
            
            # Register Search and Play
            self._register_youtube_play_tool(add_tool, PropertyList, Property, PropertyType)
            
            # Register Stop
            self._register_youtube_stop_tool(add_tool, PropertyList)
            
            self._initialized = True
            logger.info("[YoutubeManager] YouTube tools registered")
        except Exception as e:
            logger.error(f"[YoutubeManager] Registration failed: {e}")

    def _register_youtube_play_tool(self, add_tool, PropertyList, Property, PropertyType):
        async def youtube_play_wrapper(args: Dict[str, Any]) -> str:
            query = args.get("query", "")
            if not query:
                return "Vui lòng cung cấp tên bài hát hoặc từ khóa tìm kiếm."
            result = await self._youtube_player.search_and_play(query)
            return result.get("message", "Đã thực hiện")

        props = PropertyList([Property("query", PropertyType.STRING, description="Tên bài hát, ca sĩ hoặc từ khóa tìm kiếm trên YouTube")])
        add_tool(("youtube.play", "Tìm kiếm và phát âm thanh từ YouTube. Rất hiệu quả để tìm nhạc Việt Nam và các nội dung âm thanh mới nhất.", props, youtube_play_wrapper))

    def _register_youtube_stop_tool(self, add_tool, PropertyList):
        async def youtube_stop_wrapper(args: Dict[str, Any]) -> str:
            result = await self._youtube_player.stop()
            return result.get("message", "Đã dừng")

        add_tool(("youtube.stop", "Dừng phát nhạc từ YouTube.", PropertyList(), youtube_stop_wrapper))

_youtube_tools_manager = None

def get_youtube_tools_manager() -> YoutubeToolsManager:
    global _youtube_tools_manager
    if _youtube_tools_manager is None:
        _youtube_tools_manager = YoutubeToolsManager()
    return _youtube_tools_manager
