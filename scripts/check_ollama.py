
"""Check whether Ollama is ready for StudyBuddy AI.

This is a standalone diagnostic tool.
It does not change or start the main application.
"""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


OLLAMA_URL = os.getenv(
    "OLLAMA_BASE_URL", "http://localhost:11434"
).rstrip("/")

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")


def check_ollama():
    print("=" * 45)
    print("StudyBuddy AI - Ollama Connection Checker")
    print("=" * 45)

    print(f"Server: {OLLAMA_URL}")
    print(f"Required model: {MODEL_NAME}")

    try:
        with urlopen(
            f"{OLLAMA_URL}/api/tags", timeout=5
        ) as response:
            data = json.load(response)

        print("[PASS] Ollama server is running.")

        models = [
            model["name"]
            for model in data.get("models", [])
        ]

        print("\nAvailable models:")
        for model in models:
            print(f" - {model}")

        if MODEL_NAME in models or (
            ":" not in MODEL_NAME
            and f"{MODEL_NAME}:latest" in models
        ):
            print("\n[PASS] Required model is installed.")
            print("[PASS] Ollama setup check completed.")
            return True

        print("\n[FAIL] Required model not found.")
        print(f"Run: ollama pull {MODEL_NAME}")
        return False

    except (URLError, HTTPError, TimeoutError) as error:
        print("\n[FAIL] Cannot connect to Ollama.")
        print(f"Error: {error}")
        print("Check that Ollama is running.")
        return False

    except (ValueError, KeyError, TypeError) as error:
        print("\n[FAIL] Unexpected Ollama API response.")
        print(f"Error: {error}")
        return False


if __name__ == "__main__":
    success = check_ollama()
    raise SystemExit(0 if success else 1)
