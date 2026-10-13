import gradio as gr
from src.services.ai_service import generate_response


STUDY_MODES = {
    "Study chat": "Help me study. Answer clearly and adapt to my level.",
    "Explain a concept": "Explain the topic step by step, with a simple example.",
    "Quiz me": "Create a short practice quiz. Ask one question at a time and wait for my answer.",
    "Summarize": "Summarize the material into concise notes with the key ideas highlighted.",
    "Make flashcards": "Turn the material into useful question-and-answer flashcards.",
}


def _respond(prompt: str, study_mode: str) -> str:
    """Add study-mode guidance and delegate the request to the AI service."""
    if not prompt or not prompt.strip():
        return "Add a question or some study material above to get started."

    instruction = STUDY_MODES.get(study_mode, STUDY_MODES["Study chat"])
    return generate_response(f"{instruction}\n\nStudent's request:\n{prompt.strip()}")


def build_ui() -> gr.Blocks:
    """
    Constructs the Gradio web interface.
    
    Architectural Principle: The UI communicates strictly with `generate_response()`
    in the AI service layer and never directly with Ollama or the model client.
    """
    css = """
    .gradio-container { background: #f4f6ef !important; }
    #study-buddy { max-width: 1180px; margin: 0 auto; }
    #study-header {
        background: linear-gradient(120deg, #123c2d 0%, #1d5a40 68%, #28704d 100%);
        border: 0; border-radius: 22px; padding: 30px 34px; color: #f7f8f2;
        margin-bottom: 20px;
    }
    #study-header h1 { color: #fff; font-size: 2rem; margin: 0 0 8px; }
    #study-header p { color: #d8e9dc; margin: 0; font-size: 1rem; }
    .study-card {
        background: #fff; border: 1px solid #e4e9df; border-radius: 18px;
        padding: 20px; box-shadow: 0 8px 24px rgba(28, 54, 39, .045);
    }
    .study-card h3 { color: #174934; margin-top: 0; }
    .study-note { color: #647568; font-size: .92rem; line-height: 1.6; }
    #study-answer { min-height: 250px; }
    #study-answer .prose { color: #26382d; }
    #study-send button {
        background: #1d5a40 !important; border-color: #1d5a40 !important;
        color: white !important; font-weight: 650;
    }
    #study-send button:hover { background: #174934 !important; }
    footer { display: none !important; }
    """

    with gr.Blocks(
        title="StudyBuddy AI | Your study space",
        theme=gr.themes.Soft(
            primary_hue="green",
            secondary_hue="emerald",
            neutral_hue="stone",
        ),
        css=css,
        elem_id="study-buddy",
    ) as demo:
        gr.Markdown(
            """
            # 🌿 StudyBuddy AI

            Your calm, focused space to understand more and study smarter.
            """,
            elem_id="study-header",
        )

        with gr.Row(equal_height=True):
            with gr.Column(scale=1, min_width=250):
                with gr.Group(elem_classes=["study-card"]):
                    gr.Markdown("### Your study toolkit")
                    gr.Markdown(
                        "Choose a way to work with your material. Ask a question, "
                        "paste in notes, or try a practice activity.",
                        elem_classes=["study-note"],
                    )
                    study_mode = gr.Dropdown(
                        choices=list(STUDY_MODES),
                        value="Study chat",
                        label="Study mode",
                        interactive=True,
                    )

                with gr.Group(elem_classes=["study-card"]):
                    gr.Markdown("### 📚 Course library")
                    gr.Markdown(
                        "Use your course notes as the basis for questions and study "
                        "activities. RAG source retrieval can be connected through "
                        "the AI service as the library is implemented.",
                        elem_classes=["study-note"],
                    )
                    gr.Markdown("**Grounded learning · RAG workspace**")

            with gr.Column(scale=2, min_width=420):
                with gr.Group(elem_classes=["study-card"]):
                    gr.Markdown("### What are you studying today?")
                    user_input = gr.Textbox(
                        lines=5,
                        placeholder=(
                            "Ask a question or paste a section of your notes…\n"
                            "For example: Explain the key ideas in this chapter."
                        ),
                        label="Your question or study material",
                        show_label=True,
                    )
                    submit_btn = gr.Button(
                        "Study with AI  →",
                        variant="primary",
                        elem_id="study-send",
                    )

                with gr.Group(elem_classes=["study-card"]):
                    gr.Markdown("### ✨ Your study guide")
                    output_box = gr.Markdown(
                        "Your explanation, summary, quiz, or flashcards will appear here.",
                        elem_id="study-answer",
                    )

        # Connect UI actions exclusively to the service layer function.
        submit_btn.click(
            fn=_respond,
            inputs=[user_input, study_mode],
            outputs=output_box,
        )
        user_input.submit(
            fn=_respond,
            inputs=[user_input, study_mode],
            outputs=output_box,
        )

    return demo
