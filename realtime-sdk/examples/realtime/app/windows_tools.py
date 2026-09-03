import subprocess
import urllib.parse
import webbrowser
from datetime import datetime

from agents import function_tool


@function_tool
def open_chrome() -> str:
    """Open Google Chrome on the user's Windows computer."""

    subprocess.Popen(
        ["cmd", "/c", "start", "", "chrome"],
        shell=False,
    )

    return "Google Chrome was opened successfully."


@function_tool
def open_youtube() -> str:
    """Open YouTube in the default web browser."""

    webbrowser.open("https://www.youtube.com")

    return "YouTube was opened successfully."


@function_tool
def open_notepad() -> str:
    """Open Windows Notepad."""

    subprocess.Popen(["notepad.exe"])

    return "Notepad was opened successfully."


@function_tool
def open_calculator() -> str:
    """Open the Windows Calculator."""

    subprocess.Popen(["calc.exe"])

    return "Calculator was opened successfully."


@function_tool
def search_google(query: str) -> str:
    """
    Search Google for the user's requested query.

    Args:
        query: The exact phrase to search for.
    """

    encoded_query = urllib.parse.quote_plus(query)

    webbrowser.open(
        f"https://www.google.com/search?q={encoded_query}"
    )

    return f"Google search opened for: {query}"


@function_tool
def get_current_time() -> str:
    """Return the user's current local time."""

    current_time = datetime.now().strftime("%H:%M")

    return f"The current local time is {current_time}."