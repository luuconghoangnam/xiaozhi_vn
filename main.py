import asyncio
import sys
import os
from pathlib import Path

# Them thu muc src vao he thong
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.application import Application
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

async def main():
    try:
        # Khoi tao ung dung
        app = Application.get_instance()
        
        # Chay ung dung (mac dinh dung websocket va giao dien gui)
        # Ban co the doi mode="console" neu muon chay trong bang den
        exit_code = await app.run(protocol="websocket", mode="gui")
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        logger.info("Dang dung ung dung...")
    except Exception as e:
        logger.error(f"Loi khoi dong: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
