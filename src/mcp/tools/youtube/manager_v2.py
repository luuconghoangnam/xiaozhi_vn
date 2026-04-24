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

            self._register_youtube_play_tool(add_tool, PropertyList, Property, PropertyType)
            self._register_youtube_stop_tool(add_tool, PropertyList)

            self._initialized = True
            logger.info("[YoutubeManager] YouTube tools registered")
        except Exception as e:
            logger.error(f"[YoutubeManager] Registration failed: {e}", exc_info=True)

    def _register_youtube_play_tool(self, add_tool, PropertyList, Property, PropertyType):
        async def youtube_play_wrapper(args: Dict[str, Any]) -> str:
            query = (args.get("query") or "").strip()
            if not query:
                return "Thieu query"
            result = await self._youtube_player.search_and_play(query)
            return result.get("message", "OK")

        props = PropertyList([Property("query", PropertyType.STRING)])
        add_tool(
            (
                "youtube.play",
                "Search and play audio from YouTube by keyword.",
                props,
                youtube_play_wrapper,
            )
        )

    def _register_youtube_stop_tool(self, add_tool, PropertyList):
        async def youtube_stop_wrapper(args: Dict[str, Any]) -> str:
            result = await self._youtube_player.stop()
            return result.get("message", "Stopped")

        add_tool(("youtube.stop", "Stop YouTube playback.", PropertyList(), youtube_stop_wrapper))


_youtube_tools_manager = None


def get_youtube_tools_manager() -> YoutubeToolsManager:
    global _youtube_tools_manager
    if _youtube_tools_manager is None:
        _youtube_tools_manager = YoutubeToolsManager()
    return _youtube_tools_manager

