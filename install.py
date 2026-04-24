import os
import subprocess
import sys
import shutil
from pathlib import Path

def print_step(msg):
    print(f"\n[>>>] {msg}")

def run_command(cmd, shell=True):
    try:
        subprocess.check_call(cmd, shell=shell)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {cmd}")
        return False

def setup():
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)

    print_step("Checking Python version...")
    if sys.version_info < (3, 9) or sys.version_info >= (3, 13):
        print("Warning: Python 3.9 - 3.12 is recommended.")
    
    # 1. Create Virtual Environment
    if not os.path.exists(".venv"):
        print_step("Creating virtual environment...")
        if not run_command(f'"{sys.executable}" -m venv .venv'):
            return

    # 2. Determine pip path
    if os.name == "nt":
        pip_path = os.path.join(".venv", "Scripts", "pip")
        python_path = os.path.join(".venv", "Scripts", "python")
    else:
        pip_path = os.path.join(".venv", "bin", "pip")
        python_path = os.path.join(".venv", "bin", "python")

    # 3. Upgrade pip
    print_step("Upgrading pip...")
    run_command(f'"{python_path}" -m pip install --upgrade pip')

    # 4. Install Requirements
    print_step("Installing dependencies (this may take a while)...")
    if not run_command(f'"{pip_path}" install -r requirements.txt'):
        print("Error: Failed to install requirements.")
        return

    # 5. Setup Config
    config_dir = project_root / "config"
    config_file = config_dir / "config.json"
    example_config = config_dir / "config.example.json"

    if not config_file.exists():
        if example_config.exists():
            print_step("Creating config.json from example...")
            shutil.copy(example_config, config_file)
            print("Done: Please edit config/config.json with your own credentials.")
        else:
            print("Error: config.example.json not found!")
    else:
        print_step("config.json already exists, skipping.")

    # 6. Check Models
    models_dir = project_root / "models"
    required_models = ["encoder.onnx", "decoder.onnx", "joiner.onnx", "tokens.txt"]
    missing_models = [m for m in required_models if not (models_dir / m).exists()]

    if missing_models:
        print_step("Warning: Some model files are missing in the /models directory!")
        print(f"Missing: {', '.join(missing_models)}")
        print("Please download Sherpa-ONNX models and place them in the /models folder.")
    else:
        print_step("All basic model files found.")

    print_step("Installation Successful!")
    print("\nTo run the application:")
    if os.name == "nt":
        print("1. .venv\\Scripts\\activate")
    else:
        print("1. source .venv/bin/activate")
    print("2. python main.py")

if __name__ == "__main__":
    setup()
