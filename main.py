import sys
import asyncio
from pathlib import Path

# Them thu muc src vao he thong
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.application import Application
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

async def start_app():
    try:
        app_instance = Application.get_instance()
        # THU NGHIEM: Chay o che do 'console' de tranh loi GUI
        exit_code = await app_instance.run(protocol="websocket", mode="console")
        return exit_code
    except Exception as e:
        logger.error(f"Loi: {e}", exc_info=True)
        return 1

def main():
    try:
        asyncio.run(start_app())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Loi nghiem trong: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
