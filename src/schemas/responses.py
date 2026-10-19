from pydantic import BaseModel, Field
from src.config import config


class UserRequest(BaseModel):
    """Validate and bound prompts before they reach the model."""

    message: str = Field(
        ..., min_length=1, max_length=config.max_prompt_chars,
        description=f"The user's prompt or message (up to {config.max_prompt_chars:,} characters).",
    )


class AIResponse(BaseModel):
    """Minimal schema for structured response output from the AI service layer."""

    content: str = Field(..., description="The generated response text or user-friendly error message.")
    success: bool = Field(True, description="Flag indicating if the operation succeeded.")
    error_message: str | None = Field(None, description="Detailed error description if success is False.")
