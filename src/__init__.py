"""Core package API for the Ollama-powered StudyBuddy AI application.

Keep UI code dependent on the service layer rather than calling the model
client directly. The commonly used service and response types are re-exported
here for convenient imports from application code and tests.
"""

from src.schemas.responses import AIResponse, UserRequest
from src.services.ai_service import AIService, generate_response

__all__ = [
	"AIResponse",
	"AIService",
	"UserRequest",
	"generate_response",
]
