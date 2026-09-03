import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

import wake_word


BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "realtime-sdk" / "examples" / "realtime" / "app"
ENV_FILE = BASE_DIR / ".env"
SERVER_URL = "http://127.0.0.1:8000"


def server_is_ready():
    try:
        urllib.request.urlopen(SERVER_URL, timeout=1)
        return True
    except Exception:
        return False


def start_server():
    load_dotenv(ENV_FILE)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY was not found in .env"
        )

    environment = os.environ.copy()
    environment["OPENAI_API_KEY"] = api_key

    process = subprocess.Popen(
        [sys.executable, "server.py"],
        cwd=APP_DIR,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    for _ in range(120):
        if server_is_ready():
            return process

        if process.poll() is not None:
            raise RuntimeError("NOVA server failed to start.")

        time.sleep(0.25)

    process.terminate()
    raise RuntimeError("NOVA server startup timed out.")


def main():
    server_process = None

    try:
        if not server_is_ready():
            server_process = start_server()

        wake_word.main()

    finally:
        if server_process is not None:
            server_process.terminate()


if __name__ == "__main__":
    main()