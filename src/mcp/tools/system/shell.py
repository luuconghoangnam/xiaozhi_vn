import subprocess
from typing import Any, Dict

async def run_shell_command(args: Dict[str, Any]) -> str:
    """
    Run a shell command and return the output.
    """
    command = args.get("command", "")
    if not command:
        return "Vui lòng cung cấp lệnh cần chạy."
    
    try:
        # Run command safely
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        output = stdout.decode('utf-8', errors='ignore')
        error = stderr.decode('utf-8', errors='ignore')
        
        result = ""
        if output:
            result += f"Kết quả:\n{output}\n"
        if error:
            result += f"Lỗi:\n{error}\n"
            
        if not result:
            result = "Lệnh đã thực thi nhưng không có đầu ra."
            
        return result
    except Exception as e:
        return f"Lỗi khi thực thi lệnh: {str(e)}"

# Since it needs asyncio, we'll import it inside or at top
import asyncio
