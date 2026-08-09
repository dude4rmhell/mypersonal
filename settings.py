from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - graceful fallback when dependency is absent
    def load_dotenv(*_args, **_kwargs):
        return False


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

APP_NAME = "Helios"
VERSION = "0.6.0"
PLUGIN_VERSION = "0.6.0"
DEFAULT_PROVIDER = os.getenv("HELIOS_DEFAULT_PROVIDER", "groq").strip().lower()
DEFAULT_TEMPERATURE = float(os.getenv("HELIOS_DEFAULT_TEMPERATURE", "0.2"))
DEFAULT_MAX_TOKENS = int(os.getenv("HELIOS_DEFAULT_MAX_TOKENS", "1024"))
REQUEST_TIMEOUT = float(os.getenv("HELIOS_REQUEST_TIMEOUT", "30"))
MAX_CONVERSATION_MESSAGES = int(os.getenv("HELIOS_MAX_CONVERSATION_MESSAGES", "50"))
HISTORY_LIMIT = int(os.getenv("HELIOS_HISTORY_LIMIT", "50"))

LOG_PATH = BASE_DIR / "logs" / "helios.log"
AUTOMATION_LOG_PATH = BASE_DIR / "logs" / "automation.log"
CONVERSATION_PATH = BASE_DIR / "memory" / "conversation.json"
USAGE_PATH = BASE_DIR / "memory" / "usage.json"
EXPORT_DIR = BASE_DIR / "memory" / "exports"
RUNTIME_CONFIG_PATH = BASE_DIR / "config" / "runtime.json"
PLUGIN_ROOT = BASE_DIR / "plugins"
SCREENSHOT_DIR = BASE_DIR / "screenshots"

PROVIDER_SETTINGS = {
    "groq": {
        "api_key_env": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        "models": [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
        ],
        "needs_api_key": True,
    },
    "openrouter": {
        "api_key_env": "OPENROUTER_API_KEY",
        "base_url": "https://openrouter.ai/api/v1",
        "default_model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        "models": [
            "openai/gpt-4o-mini",
            "openai/gpt-4.1-mini",
            "anthropic/claude-3.5-sonnet",
            "google/gemini-2.0-flash-001",
            "meta-llama/llama-3.3-70b-instruct",
        ],
        "needs_api_key": True,
    },
    "openai": {
        "api_key_env": "OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1",
        "default_model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "models": [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4.1-mini",
            "gpt-4.1",
        ],
        "needs_api_key": True,
    },
    "local": {
        "api_key_env": "",
        "base_url": os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/v1"),
        "default_model": os.getenv("LOCAL_LLM_MODEL", "llama3.1"),
        "models": [
            "llama3.1",
            "qwen2.5",
            "gemma3",
            "phi3",
        ],
        "needs_api_key": False,
    },
}
