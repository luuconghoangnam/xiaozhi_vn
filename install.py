import os
import subprocess
import sys
import shutil
import urllib.request
import zipfile
from pathlib import Path

# URL tải model từ Release chính chủ của bạn
MODEL_URL = "https://github.com/luuconghoangnam/xiaozhi_vn/releases/download/v1.0.0/models_vn.zip"

def print_step(msg):
    print(f"\n[>>>] {msg}")

def run_command(cmd, shell=True):
    try:
        subprocess.check_call(cmd, shell=shell)
        return True
    except subprocess.CalledProcessError:
        return False

def download_file(url, dest):
    print(f"Downloading {url}...")
    try:
        urllib.request.urlretrieve(url, dest)
        return True
    except Exception as e:
        print(f"Error downloading: {e}")
        return False

def setup():
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)

    print_step("Checking Python version...")
    if sys.version_info < (3, 9):
        print("Error: Python 3.9+ is required.")
        return

    # 1. Create Virtual Environment
    if not os.path.exists(".venv"):
        print_step("Creating virtual environment...")
        run_command(f'"{sys.executable}" -m venv .venv')

    # 2. Determine paths
    if os.name == "nt":
        pip_path = os.path.join(".venv", "Scripts", "pip")
        python_path = os.path.join(".venv", "Scripts", "python")
    else:
        pip_path = os.path.join(".venv", "bin", "pip")
        python_path = os.path.join(".venv", "bin", "python")

    # 3. Install Requirements
    print_step("Installing Python dependencies (this may take 1-2 minutes)...")
    run_command(f'"{pip_path}" install --upgrade pip')
    if not run_command(f'"{pip_path}" install -r requirements.txt'):
        print("Error: Failed to install requirements.")
        return

    # 4. Setup Config
    config_dir = project_root / "config"
    config_file = config_dir / "config.json"
    example_config = config_dir / "config.example.json"

    if not config_file.exists():
        if example_config.exists():
            print_step("Initializing config.json...")
            shutil.copy(example_config, config_file)
            print("Done: Please edit config/config.json with your Access Token.")
    
    # 5. Download Models Automatically
    models_dir = project_root / "models"
    models_dir.mkdir(exist_ok=True)
    
    # Kiểm tra xem đã có model chưa (ví dụ file encoder.onnx)
    if not (models_dir / "encoder.onnx").exists():
        print_step("Downloading AI models (Sherpa-ONNX VN)...")
        zip_dest = project_root / "models_temp.zip"
        if download_file(MODEL_URL, zip_dest):
            print("Extracting models...")
            with zipfile.ZipFile(zip_dest, 'r') as zip_ref:
                zip_ref.extractall(models_dir)
            os.remove(zip_dest)
            print("Models installed successfully.")
        else:
            print("Failed to download models automatically. Please check your internet connection.")
    else:
        print_step("Models already exist, skipping download.")

    # 6. Driver/FFmpeg Check (Windows)
    if os.name == "nt":
        print_step("Checking for FFmpeg (required for audio/YouTube)...")
        ffmpeg_exists = run_command("ffmpeg -version")
        if not ffmpeg_exists:
            print("Notice: FFmpeg not found in system PATH.")
            print("Tip: You can download it from https://ffmpeg.org/ or use 'choco install ffmpeg'.")

    print_step("INSTALLATION COMPLETE!")
    print("\nHow to start:")
    print(f"1. Activate venv: {'.venv\\Scripts\\activate' if os.name == 'nt' else 'source .venv/bin/activate'}")
    print("2. Run app: python main.py")

if __name__ == "__main__":
    setup()
