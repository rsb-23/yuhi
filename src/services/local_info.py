import subprocess


def get_git_user() -> str:
    result = subprocess.run(["git", "config", "--get", "user.name"], capture_output=True, text=True, check=True)
    return result.stdout.strip() if result.returncode == 0 else ""
