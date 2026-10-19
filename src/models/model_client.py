from typing import Optional
import ollama
from src.config import config


class ModelClientError(Exception):
    """Base exception for model client failures."""
    pass


class OllamaConnectionError(ModelClientError):
    """Exception raised when Ollama service is unreachable."""
    pass


class ModelNotFoundError(ModelClientError):
    """Exception raised when the requested model is not found on local Ollama."""
    pass


class OllamaModelClient:
    """Encapsulates interaction with local Ollama inference server."""

    def __init__(self, base_url: Optional[str] = None, model_name: Optional[str] = None):
        self.base_url = base_url or config.ollama_base_url
        self.model_name = model_name or config.model_name
        self._client = ollama.Client(
            host=self.base_url,
            timeout=config.model_timeout_seconds,
        )

    def generate(self, prompt: str) -> str:
        """
        Sends a user prompt to local Ollama model and returns generated response text.
        
        Raises ModelClientError subclass if connection or execution fails.
        """
        try:
            response = self._client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            
            # Standardize extraction from dict or chat response object.
            if isinstance(response, dict):
                message = response.get("message") or {}
                content = message.get("content", "") if isinstance(message, dict) else ""
            elif hasattr(response, "message") and hasattr(response.message, "content"):
                content = response.message.content
            else:
                content = ""

            if not isinstance(content, str) or not content.strip():
                raise ModelClientError("The model returned an empty response.")
            return content.strip()

        except Exception as err:
            if isinstance(err, ModelClientError):
                raise
            err_str = str(err).lower()
            status_code = getattr(err, "status_code", None)
            if status_code == 404 or "model" in err_str and ("not found" in err_str or "pull" in err_str):
                raise ModelNotFoundError(
                    f"Model '{self.model_name}' is not installed in local Ollama."
                ) from err
            if (
                isinstance(err, (ConnectionError, TimeoutError))
                or any(term in err_str for term in ("connection", "connect", "refused", "timed out", "timeout"))
            ):
                raise OllamaConnectionError(
                    f"Could not reach Ollama at {self.base_url} within "
                    f"{config.model_timeout_seconds:g} seconds."
                ) from err
            raise ModelClientError(f"Error communicating with Ollama: {err}") from err
