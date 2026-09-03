import json
import os
import queue
import time
from pathlib import Path

import pygame
import sounddevice as sd
from dotenv import load_dotenv
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from vosk import KaldiRecognizer, Model, SetLogLevel


SAMPLE_RATE = 16000
NOVA_URL = "http://localhost:8000"

WAKE_PHRASES = {
    "hey nova",
    "nova",
    "hey no va",
    "no va",
    "okay nova",
    "a nova",
}

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "MODELS"
WAKE_AUDIO_FILE = BASE_DIR / "nova_wake.mp3"

load_dotenv(BASE_DIR / ".env")

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY was not found in the .env file.")

client = OpenAI()
SetLogLevel(-1)


def find_vosk_model() -> Path:
    for model_file in MODELS_DIR.rglob("final.mdl"):
        model_root = model_file.parent.parent

        if (model_root / "conf" / "mfcc.conf").exists():
            return model_root

    raise FileNotFoundError(
        "Vosk model was not found inside the MODELS folder."
    )


def contains_wake_phrase(text: str) -> bool:
    normalized = " ".join(text.lower().strip().split())
    return any(phrase in normalized for phrase in WAKE_PHRASES)


def wait_for_wake_word(model: Model) -> None:
    audio_queue: queue.Queue[bytes] = queue.Queue()

    grammar = json.dumps(
        [
            "hey nova",
            "nova",
            "hey no va",
            "no va",
            "okay nova",
            "a nova",
            "[unk]",
        ]
    )

    recognizer = KaldiRecognizer(model, SAMPLE_RATE, grammar)

    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"Microphone warning: {status}")

        audio_queue.put(bytes(indata))

    print("NOVA is sleeping. Say: Hey NOVA")

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=4000,
        dtype="int16",
        channels=1,
        callback=audio_callback,
    ):
        while True:
            audio_data = audio_queue.get()

            if recognizer.AcceptWaveform(audio_data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()
            else:
                result = json.loads(recognizer.PartialResult())
                text = result.get("partial", "").strip()

            if contains_wake_phrase(text):
                print(f"Wake word detected: {text}")
                return


def acknowledge_wake_word() -> None:
    try:
        if not WAKE_AUDIO_FILE.exists():
            with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice="ash",
                input="بله قربان.",
                instructions=(
                    "Speak in natural conversational Iranian Persian. "
                    "Use a mature, deep, calm masculine voice. "
                    "Sound attentive and subtly confident. "
                    "Say only the supplied words."
                ),
                response_format="mp3",
            ) as response:
                response.stream_to_file(WAKE_AUDIO_FILE)

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(str(WAKE_AUDIO_FILE))
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.05)

        pygame.mixer.music.unload()

    except Exception as error:
        print(f"NOVA wake response error: {error}")


def launch_nova() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.media_stream_mic": 1,
        },
    )
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get(NOVA_URL)

    connect_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(normalize-space(.), 'Connect')]",
            )
        )
    )
    connect_button.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//button[contains(normalize-space(.), 'Disconnect')]",
            )
        )
    )

    print("NOVA: Realtime connected.")
    return driver


def keep_session_open(driver: webdriver.Chrome) -> None:
    print("NOVA is online. Close its Chrome window to return to sleep mode.")

    while True:
        try:
            if not driver.window_handles:
                return

            time.sleep(1)

        except Exception:
            return


def main() -> None:
    model_path = find_vosk_model()
    print(f"Wake-word model: {model_path.name}")

    model = Model(str(model_path))

    while True:
        driver = None

        try:
            wait_for_wake_word(model)
            acknowledge_wake_word()
            driver = launch_nova()
            keep_session_open(driver)

        except KeyboardInterrupt:
            print("\nNOVA: Shutting down.")
            break

        except Exception as error:
            print(f"NOVA Error: {error}")
            time.sleep(2)

        finally:
            if driver is not None:
                try:
                    driver.quit()
                except Exception:
                    pass

        print("NOVA returned to sleep mode.")


if __name__ == "__main__":
    main()
