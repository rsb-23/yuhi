import subprocess


def get_git_user() -> str:
    try:
        result = subprocess.run(["git", "config", "--get", "user.name"], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        return ""
    return result.stdout.strip()
