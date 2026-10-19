from unittest.mock import MagicMock, patch

import pytest

from src.models.model_client import (
    ModelClientError,
    ModelNotFoundError,
    OllamaConnectionError,
    OllamaModelClient,
)


def make_client(chat_response=None, error=None):
    mock_ollama = MagicMock()
    mock_ollama.chat.return_value = chat_response
    if error is not None:
        mock_ollama.chat.side_effect = error
    with patch("src.models.model_client.ollama.Client") as client_factory:
        client_factory.return_value = mock_ollama
        client = OllamaModelClient(base_url="http://ollama.test", model_name="test-model")
    return client, mock_ollama


def test_generate_sends_chat_prompt_and_returns_content():
    client, mock_ollama = make_client({"message": {"content": "  Study answer  "}})

    assert client.generate("Explain gravity") == "Study answer"
    mock_ollama.chat.assert_called_once_with(
        model="test-model",
        messages=[{"role": "user", "content": "Explain gravity"}],
    )


def test_empty_model_response_is_a_controlled_error():
    client, _ = make_client({"message": {"content": "  "}})

    with pytest.raises(ModelClientError, match="empty response"):
        client.generate("Explain gravity")


def test_missing_model_is_classified():
    error = RuntimeError("model 'test-model' not found")
    client, _ = make_client(error=error)

    with pytest.raises(ModelNotFoundError):
        client.generate("Explain gravity")


def test_connection_failure_is_classified():
    client, _ = make_client(error=ConnectionError("connection refused"))

    with pytest.raises(OllamaConnectionError, match="Could not reach Ollama"):
        client.generate("Explain gravity")
