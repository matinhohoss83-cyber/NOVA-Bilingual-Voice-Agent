# NOVA - Bilingual Desktop Voice Agent

NOVA is an experimental Persian-English AI voice assistant for Windows.

> Independent AI Systems Research Project

## Features

- Offline Hey NOVA wake-word detection
- Real-time Persian and English voice conversations
- Spoken acknowledgement after activation
- Voice-controlled Windows automation
- Opens Chrome, YouTube, Notepad, and Calculator
- Performs Google searches through voice commands
- Automatic startup with Windows
- Configurable personality and response style

## Architecture

NOVA uses a hybrid local-cloud architecture.

1. Vosk detects the wake phrase locally.
2. NOVA acknowledges the user.
3. A local Realtime server starts.
4. The voice interface connects to the AI model.
5. The agent interprets the request.
6. Approved Windows tools execute the action.

## Research Focus

This project explores bilingual Persian-English voice interaction, code-switching, local wake-word processing, response latency, API cost, privacy, and reliable desktop automation.

Formal benchmark results will be published after testing. No unverified performance claims are included.

## Technology

- Python
- OpenAI Realtime API
- OpenAI Agents SDK
- Vosk
- Selenium
- FastAPI
- WebSockets
- Windows automation

## Installation

Create a Python virtual environment and install the dependencies from requirements.txt.

Create a .env file and add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here

Download a compatible Vosk model and place it inside a folder named MODELS.

Run the assistant with:

python nova.py

## Security

- API keys are excluded from GitHub.
- Wake-word detection runs locally.
- Sensitive actions should require confirmation.
- Tool access is limited to approved functions.

## Roadmap

- Animated NOVA interface
- Improved Persian wake-word recognition
- Persistent user-controlled memory
- Action confirmations and audit logs
- Bilingual benchmark dataset
- Latency and API-cost evaluation
- Packaged Windows application

## Status

Active prototype under development.

## Author

Matin Hosseini

AI Systems Developer - Independent Research Project
