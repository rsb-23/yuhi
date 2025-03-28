import os
import subprocess
import sys

from src.helper.color_path import Path

venv_path = Path.cwd() / "venv"


def run_in_venv(cmd: str, check=True):
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(venv_path)
    env["PATH"] = str(Path.cwd()) + env["PATH"]

    subprocess.run(cmd, env=env, check=check, shell=True)


def create_venv(venv_dir=".venv"):
    # TODO: this is temp code
    venv_dir = Path(venv_dir)
    # Create the virtual environment
    if not os.path.exists(venv_dir):
        subprocess.run([sys.executable, "-m", "venv", venv_dir.name], check=True)
        print(f"Virtual environment created at {venv_dir}")
    else:
        print(f"Virtual environment already exists at {venv_dir}")

    if venv_dir.joinpath("Scripts").exists():
        subprocess.run([f"{venv_dir.name}/Scripts/activate"], check=True)
    else:
        subprocess.run([f"source {venv_dir.name}/bin/activate"], check=True)


def install_requirements(venv_dir="venv", requirements_file="requirements.txt"):
    # TODO: this is temp code
    # Path to pip in the virtual environment
    pip_executable = (
        os.path.join(venv_dir, "Scripts", "pip") if os.name == "nt" else os.path.join(venv_dir, "bin", "pip")
    )

    if os.path.exists(requirements_file):
        subprocess.run([pip_executable, "install", "-r", requirements_file], check=True)
        print(f"Installed requirements from {requirements_file}")
    else:
        print(f"Requirements file {requirements_file} not found.")


if __name__ == "__main__":
    VENV_DIRECTORY = ".venv"  # Change as needed
    REQ_FILE = "requirements.txt"  # Change as needed

    create_venv(VENV_DIRECTORY)
    install_requirements(VENV_DIRECTORY, REQ_FILE)
