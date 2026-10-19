import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


@dataclass
class Config:
    """Simple configuration object reading environment variables."""

    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model_name: str = os.getenv("MODEL_NAME", "llama3.2")
    model_timeout_seconds: float = float(os.getenv("MODEL_TIMEOUT_SECONDS", "120"))
    max_prompt_chars: int = int(os.getenv("MAX_PROMPT_CHARS", "16000"))


# Instantiate global configuration object
config = Config()
