import sys
import asyncio
from pathlib import Path
from PyQt5.QtWidgets import QApplication
import qasync

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
        # Chay app voi che do GUI
        exit_code = await app_instance.run(protocol="websocket", mode="gui")
        return exit_code
    except Exception as e:
        logger.error(f"Loi trong qua trinh chay: {e}", exc_info=True)
        return 1

def main():
    # 1. Khoi tao QApplication (bat buoc cho PyQt5)
    qt_app = QApplication(sys.argv)
    
    # 2. Su dung qasync de ket hop asyncio va Qt
    loop = qasync.QEventLoop(qt_app)
    asyncio.set_event_loop(loop)
    
    try:
        # 3. Chay loop cho den khi app ket thuc
        with loop:
            sys.exit(loop.run_until_complete(start_app()))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Loi nghiem trong: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
