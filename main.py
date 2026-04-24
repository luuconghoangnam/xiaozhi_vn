import sys
import asyncio
from pathlib import Path
import traceback

# Tu dong nhan dien thu muc hien tai
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def main():
    try:
        from src.application import Application
        from src.utils.logging_config import get_logger
        
        logger = get_logger(__name__)
        
        async def start_app():
            try:
                app_instance = Application.get_instance()
                # Chay o che do console de bat loi
                exit_code = await app_instance.run(protocol="websocket", mode="console")
                return exit_code
            except Exception as e:
                print(f"\n[!] LOI: {e}")
                traceback.print_exc()
                return 1

        asyncio.run(start_app())
        
    except Exception as e:
        print(f"\n[!] LOI KHOI DONG: {e}")
        traceback.print_exc()
        with open("crash_report.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
