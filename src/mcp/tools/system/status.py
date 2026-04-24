import psutil
import platform
import os
from typing import Any, Dict

def get_computer_status(args: Dict[str, Any]) -> str:
    """
    Get the current computer status (CPU, RAM, Disk, etc.)
    """
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        status = (
            f"=== Trạng thái máy tính ===\n"
            f"- Hệ điều hành: {platform.system()} {platform.release()}\n"
            f"- CPU Usage: {cpu_usage}%\n"
            f"- RAM Usage: {memory.percent}% ({memory.used // (1024**2)}MB / {memory.total // (1024**2)}MB)\n"
            f"- Disk Usage: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)\n"
        )
        
        # Optional: Battery info if laptop
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()
            if battery:
                status += f"- Pin: {battery.percent}% ({'Đang sạc' if battery.power_plugged else 'Không sạc'})\n"
                
        return status
    except Exception as e:
        return f"Lỗi khi lấy trạng thái máy tính: {str(e)}"
