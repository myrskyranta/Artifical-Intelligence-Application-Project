import gradio as gr
from src.capabilities.rag import DocumentLibrary, DocumentProcessingError
from src.services.ai_service import generate_response


STUDY_MODES = {
    "Study chat": "Help me study. Answer clearly and adapt to my level.",
    "Explain a concept": "Explain the topic step by step, with a simple example.",
    "Quiz me": (
        "Quiz the student on the supplied topic or material, one question at a time. Wait for their "
        "answer, give brief feedback grounded in the material, then ask the next question."
    ),
    "Summarize": "Summarize the material into concise notes with the key ideas highlighted.",
    "Make flashcards": "Turn the material into useful question-and-answer flashcards.",
}

MODE_DESCRIPTIONS = {
    "Study chat": "Ask a question and get a clear explanation tailored to your level.",
    "Explain a concept": "Break a difficult idea into steps and see it in a simple example.",
    "Quiz me": "Answer one question at a time; I’ll check your answer against the uploaded notes.",
    "Summarize": "Turn a longer passage into concise notes and key takeaways.",
    "Make flashcards": "Create question-and-answer cards to help you review.",
}

WELCOME_MESSAGE = (
    "Hi! Upload some course material, choose a study mode, and ask me to explain, "
    "summarize, or quiz you on it."
)


def _respond(
    prompt: str,
    study_mode: str,
    document_library: DocumentLibrary | None = None,
    history: list[dict[str, str]] | None = None,
) -> tuple[list[dict[str, str]], str]:
    """Add study-mode guidance and delegate the request to the AI service."""
    conversation = list(history or [])
    if not prompt or not prompt.strip():
        return conversation, ""

    instruction = STUDY_MODES.get(study_mode, STUDY_MODES["Study chat"])
    recent_turns = conversation[-8:]
    prior_context = "\n".join(
        f"{message.get('role', 'assistant').title()}: {message.get('content', '')}"
        for message in recent_turns
        if isinstance(message.get("content"), str)
    )
    request = f"{instruction}\n\n"
    if prior_context:
        request += (
            "Continue this study conversation and use the previous turns for context. "
            "For quizzes, remember the question asked, assess the student's latest answer, "
            "and then continue with a new question.\n"
            f"Previous turns:\n{prior_context}\n\n"
        )
    request += f"Student's latest request:\n{prompt.strip()}"
    context = document_library.retrieve(f"{prompt}\n{prior_context}") if document_library else None
    answer = generate_response(request, context=context)
    conversation.extend(
        [
            {"role": "user", "content": prompt.strip()},
            {"role": "assistant", "content": answer},
        ]
    )
    return conversation, ""


def _clear_session() -> tuple[str, list[dict[str, str]]]:
    """Clear the current prompt and chat while leaving uploaded materials intact."""
    return "", [{"role": "assistant", "content": WELCOME_MESSAGE}]


def _load_materials(files) -> tuple[str, DocumentLibrary | None]:
    """Build a session-local searchable index from the selected upload paths."""
    if not files:
        return "No documents uploaded yet. Add course notes to ground your study session.", None

    if isinstance(files, str):
        files = [files]
    try:
        library = DocumentLibrary.from_files(files)
    except DocumentProcessingError as err:
        return f"⚠️ {err}", None

    names = ", ".join(library.document_names)
    return (
        f"✅ Loaded {len(library.document_names)} document(s) · {len(library.chunks)} searchable sections\n\n"
        f"{names}",
        library,
    )


def _mode_description(study_mode: str) -> str:
    """Return a short explanation of the selected study mode."""
    return MODE_DESCRIPTIONS.get(study_mode, MODE_DESCRIPTIONS["Study chat"])


def _ui_css() -> str:
    return """
    .gradio-container {
        color-scheme: light !important;
        background: #f4f6f1 !important;
    }
    #study-buddy { max-width: 1180px; margin: 0 auto; }
    #study-header {
        background: linear-gradient(120deg, #123c2d 0%, #1d5a40 68%, #28704d 100%);
        border: 0; border-radius: 22px; padding: 30px 34px; color: #f7f8f2;
        margin-bottom: 18px;
    }
    #study-header h1 { color: #fff; font-size: 2rem; margin: 0 0 8px; }
    #study-header p { color: #d8e9dc; margin: 0; font-size: 1rem; }
    .study-card {
        background: #fff !important; color: #26382d !important;
        border: 1px solid #e4e9df; border-radius: 18px;
        padding: 26px !important; margin-bottom: 12px;
        box-shadow: 0 8px 24px rgba(28, 54, 39, .045);
        --body-text-color: #26382d;
        --block-background-fill: #ffffff;
        --block-label-text-color: #385945;
        --input-background-fill: #fbfdfb;
    }
    .study-card .block, .study-card .form {
        background-color: #fff !important; color: #26382d !important;
    }
    .study-card h2, .study-card h3 {
        color: #2a704d !important; margin-top: 0; margin-bottom: 14px;
    }
    .study-card p, .study-note {
        color: #4d6254 !important; font-size: .96rem; line-height: 1.75;
    }
    .study-card p { margin-bottom: 14px; }
    #study-buddy textarea {
        background: #fbfdfb !important; color: #26382d !important;
        border-color: #cbd9ce !important; border-radius: 12px !important;
        line-height: 1.65; padding: 15px 16px !important;
    }
    #study-buddy input { color: #26382d !important; }
    #mode-help {
        background: #f1f7f1 !important; border: 1px solid #d5e5d8; border-radius: 12px;
        padding: 13px 15px; color: #315c40 !important; min-height: 52px;
    }
    #study-chatbot { min-height: 340px; }
    #study-chatbot .prose { color: #26382d; line-height: 1.7; }
    #study-send button {
        background: #1d5a40 !important; border-color: #1d5a40 !important;
        color: white !important; font-weight: 650;
    }
    #study-send button:hover { background: #174934 !important; }
    #study-clear button { min-height: 44px; }
    footer { display: none !important; }
    @media (max-width: 700px) {
        #study-header { padding: 24px 22px; border-radius: 18px; }
        #study-header h1 { font-size: 1.65rem; }
        .study-card { padding: 20px !important; }
    }
    """


def ui_launch_options() -> dict[str, object]:
    """Return theme and CSS through Gradio's supported launch options."""
    return {
        "theme": gr.themes.Soft(
            primary_hue="green",
            secondary_hue="emerald",
            neutral_hue="stone",
        ).set(
            body_background_fill="#f4f6f1",
            body_text_color="#26382d",
            block_background_fill="#ffffff",
            block_label_text_color="#385945",
            block_title_text_color="#216442",
            input_background_fill="#fbfdfb",
            input_placeholder_color="#6a7b70",
        ),
        "css": _ui_css(),
    }


def build_ui() -> gr.Blocks:
    """Construct the UI; all model requests remain behind the service layer."""
    with gr.Blocks(
        title="StudyBuddy AI | Your study space",
        elem_id="study-buddy",
    ) as demo:
        gr.Markdown(
            """
            # 🌿 StudyBuddy AI

            A calm space to understand your course material and study smarter.
            """,
            elem_id="study-header",
        )

        with gr.Row(equal_height=True):
            with gr.Column(scale=1, min_width=250):
                with gr.Group(elem_classes=["study-card"]):
                    gr.Markdown("### Choose how to study")
                    gr.Markdown(
                        "Pick a mode, then ask a question or paste in your notes.",
                        elem_classes=["study-note"],
                    )
                    study_mode = gr.Dropdown(
                        choices=list(STUDY_MODES),
                        value="Study chat",
                        label="Study mode",
                        interactive=True,
                    )
                    mode_help = gr.Markdown(
                        MODE_DESCRIPTIONS["Study chat"],
                        elem_id="mode-help",
                        elem_classes=["study-note"],
                    )

                with gr.Group(elem_classes=["study-card"]):
                    gr.Markdown("### 💡 Get a better answer")
                    gr.Markdown(
                        "Upload your course documents below, then choose a study mode. "
                        "You can also ask a specific question about the uploaded material.",
                        elem_classes=["study-note"],
                    )
                    study_files = gr.File(
                        label="Course materials",
                        file_count="multiple",
                        file_types=[".txt", ".md", ".pdf", ".docx"],
                        type="filepath",
                    )
                    document_status = gr.Markdown(
                        "No documents uploaded yet. Add course notes to ground your study session.",
                        elem_classes=["study-note"],
                    )
                    document_library = gr.State(value=None)
                    gr.Markdown(
                        "Supported: TXT, Markdown, PDF, DOCX · Up to 8 files, 20 MB each. "
                        "Scanned PDFs need selectable text (OCR is not included).",
                        elem_classes=["study-note"],
                    )
                    gr.Markdown(
                        "🔒 Documents are read locally and used for this session's answers.",
                        elem_classes=["study-note"],
                    )

            with gr.Column(scale=2, min_width=420):
                with gr.Group(elem_classes=["study-card"]):
                    gr.Markdown("### What are you studying today?")
                    user_input = gr.Textbox(
                        lines=6,
                        max_lines=12,
                        placeholder=(
                            "Ask a question or paste in a section of your notes…\n"
                            "For example: Explain the key ideas in this chapter in simple terms."
                        ),
                        label="Your question or study material",
                        show_label=False,
                    )
                    gr.Examples(
                        examples=[
                            ["Explain photosynthesis in simple terms with an example."],
                            ["Quiz me on the key ideas in my uploaded materials, one question at a time."],
                            ["Summarize this topic into key points and definitions."],
                        ],
                        inputs=[user_input],
                        label="Try an example",
                    )
                    with gr.Row():
                        submit_btn = gr.Button(
                            "Study with AI  →",
                            variant="primary",
                            elem_id="study-send",
                            scale=3,
                        )
                        clear_btn = gr.Button(
                            "Clear",
                            variant="secondary",
                            elem_id="study-clear",
                            scale=1,
                        )

                with gr.Group(elem_classes=["study-card"]):
                    gr.Markdown("### ✨ Your study session")
                    chat = gr.Chatbot(
                        value=[{"role": "assistant", "content": WELCOME_MESSAGE}],
                        height=360,
                        show_label=False,
                        elem_id="study-chatbot",
                    )

        # Connect UI actions exclusively to the service layer function.
        submit_btn.click(
            fn=_respond,
            inputs=[user_input, study_mode, document_library, chat],
            outputs=[chat, user_input],
        )
        user_input.submit(
            fn=_respond,
            inputs=[user_input, study_mode, document_library, chat],
            outputs=[chat, user_input],
        )
        study_files.change(
            fn=_load_materials,
            inputs=study_files,
            outputs=[document_status, document_library],
        )
        study_mode.change(
            fn=_mode_description,
            inputs=study_mode,
            outputs=mode_help,
        )
        clear_btn.click(
            fn=_clear_session,
            inputs=None,
            outputs=[user_input, chat],
        )

    return demo
