from typing import Optional
from pydantic import ValidationError
from src.config import config
from src.models.model_client import (
    OllamaModelClient,
    ModelClientError,
    OllamaConnectionError,
    ModelNotFoundError,
)
from src.schemas.responses import UserRequest, AIResponse


STUDY_MODES = {
    "Study chat": "Help me study. Answer clearly, accurately, and adapt to my level.",
    "Explain a concept": "Explain the topic step by step, define key terms, and give one simple example.",
    "Quiz me": "Create a short practice quiz. Ask one question at a time and wait for my answer.",
    "Summarize": "Summarize the supplied material as concise notes with the key ideas highlighted.",
    "Make flashcards": "Turn the supplied material into concise question-and-answer flashcards.",
}


class AIService:
    """
    Application service layer responsible for validating user input,
    orchestrating model client requests, and catching exceptions gracefully.
    """

    def __init__(self, model_client: Optional[OllamaModelClient] = None):
        # Allow injecting custom/mock model_client for simple testing
        self.model_client = model_client

    def _get_client(self) -> OllamaModelClient:
        """Returns active model client, initializing default client if none provided."""
        if self.model_client is None:
            self.model_client = OllamaModelClient()
        return self.model_client

    def process_message(self, user_message: str) -> AIResponse:
        """
        Processes a raw user message string and returns a structured AIResponse.
        Catches technical failures and converts them to friendly user-facing messages.
        """
        if not isinstance(user_message, str) or not user_message.strip():
            return AIResponse(
                content="Please enter a message before sending.",
                success=False,
                error_message="User message was empty.",
            )

        try:
            request = UserRequest(message=user_message.strip())
            client = self._get_client()
            response_text = client.generate(request.message)

            return AIResponse(
                content=response_text,
                success=True,
            )

        except ValidationError as err:
            return AIResponse(
                content=f"Your prompt is too long. Please keep it to {config.max_prompt_chars:,} characters or fewer.",
                success=False,
                error_message=str(err),
            )

        except OllamaConnectionError as err:
            return AIResponse(
                content=(
                    "[Error] Could not connect to Ollama.\n\n"
                    "Please verify that Ollama is installed and running locally on your machine."
                ),
                success=False,
                error_message=str(err),
            )

        except ModelNotFoundError as err:
            return AIResponse(
                content=(
                    f"[Error] The configured AI model is unavailable in Ollama.\n\n"
                    f"Please verify your MODEL_NAME setting or run 'ollama run <model_name>'."
                ),
                success=False,
                error_message=str(err),
            )

        except ModelClientError as err:
            return AIResponse(
                content="[Error] An unexpected communication error occurred with the AI model.",
                success=False,
                error_message=str(err),
            )

        except Exception as err:
            return AIResponse(
                content="[Error] An unexpected application error occurred.",
                success=False,
                error_message=str(err),
            )

    def process_study_request(self, user_message: str, study_mode: str = "Study chat") -> AIResponse:
        """Apply a study-mode instruction and process the resulting prompt."""
        instruction = STUDY_MODES.get(study_mode, STUDY_MODES["Study chat"])
        if not isinstance(user_message, str) or not user_message.strip():
            return self.process_message(user_message)
        return self.process_message(
            f"{instruction}\n\nStudent's request or study material:\n{user_message.strip()}"
        )


def generate_response(user_message: str, service: Optional[AIService] = None) -> str:
    """
    Main reusable service entry point used by the UI layer.
    
    Accepts user input message, passes it to the AI service, and returns
    the generated text response (or a friendly error message).
    """
    active_service = service or AIService()
    response = active_service.process_message(user_message)
    return response.content


def generate_study_response(
    user_message: str,
    study_mode: str = "Study chat",
    service: Optional[AIService] = None,
) -> str:
    """UI-facing entry point for study-mode requests."""
    active_service = service or AIService()
    return active_service.process_study_request(user_message, study_mode).content
