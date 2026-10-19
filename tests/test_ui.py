from unittest.mock import MagicMock

import app.ui as study_ui


def test_quiz_turn_keeps_history_and_uses_uploaded_material(monkeypatch):
    library = MagicMock()
    library.retrieve.return_value = "[Source: biology.txt]\nATP stores cellular energy."
    sent = {}

    def fake_generate_response(prompt, context=None):
        sent["prompt"] = prompt
        sent["context"] = context
        return "Correct. What molecule stores usable energy for the cell?"

    monkeypatch.setattr(study_ui, "generate_response", fake_generate_response)
    history = [
        {"role": "assistant", "content": "What is ATP's role?"},
        {"role": "user", "content": "It stores energy."},
    ]

    updated_history, cleared_prompt = study_ui._respond(
        "Give me another question.",
        "Quiz me",
        library,
        history,
    )

    assert "What is ATP's role?" in sent["prompt"]
    assert sent["context"] == "[Source: biology.txt]\nATP stores cellular energy."
    assert updated_history[-1] == {
        "role": "assistant",
        "content": "Correct. What molecule stores usable energy for the cell?",
    }
    assert updated_history[-2] == {"role": "user", "content": "Give me another question."}
    assert cleared_prompt == ""
