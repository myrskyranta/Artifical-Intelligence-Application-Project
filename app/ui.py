import gradio as gr
from src.services.ai_service import STUDY_MODES, generate_study_response


STUDY_THEME = gr.themes.Soft(
    primary_hue="green",
    secondary_hue="emerald",
    neutral_hue="stone",
    radius_size="lg",
)

STUDY_CSS = """
.gradio-container { background: #f5f3e9 !important; }
#study-buddy {
    max-width: 1180px; margin: 0 auto; padding: 22px 18px 36px;
    color-scheme: light; color: #344737;
}
#study-header {
    background: linear-gradient(125deg, #244b37 0%, #356849 72%, #66805b 100%);
    border: 0; border-radius: 28px; padding: 34px 38px; color: #f7f4ea;
    margin-bottom: 28px; box-shadow: 0 14px 34px rgba(38, 67, 47, .12);
}
#study-header h1 { color: #fff; font-size: 2rem; margin: 0 0 8px; }
#study-header p { color: #e3eadc; margin: 0; font-size: 1rem; }
.study-card {
    background: #fffef9 !important; border: 1px solid #e6e4d8 !important;
    border-radius: 26px !important; padding: 26px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 10px 28px rgba(53, 69, 45, .07) !important;
    color: #344737 !important;
}
.study-card .study-card {
    background: transparent !important; border: 0 !important;
    border-radius: 0 !important; padding: 0 !important;
    margin: 0 !important; box-shadow: none !important;
}
.study-card h3 { color: #174934; margin-top: 0; }
.study-card label span {
    color: #53694f !important; background: transparent !important;
}
.study-section-title {
    background: #477354; border-radius: 18px;
    margin-bottom: 24px !important; padding: 14px 18px;
}
.study-section-title.prose {
    background: transparent !important; border-radius: 0 !important;
    margin: 0 !important; padding: 0 !important;
}
.study-section-title h3 { color: #f7f4ea !important; margin: 0; }
.study-card .prose:not(.study-section-title) p,
.study-card .prose:not(.study-section-title) strong,
.study-card .prose:not(.study-section-title) li {
    color: #52634f !important;
}
.study-card .prose:not(.study-section-title) p {
    max-width: 100%; white-space: normal; overflow-wrap: break-word;
    word-break: normal; line-height: 1.65;
}
.study-card .study-note.prose {
    box-sizing: border-box !important;
    padding-inline: clamp(8px, 1.5vw, 18px) !important;
}
#study-input textarea,
.study-card input,
.study-card textarea {
    box-sizing: border-box !important; width: 100% !important; min-width: 0 !important;
    border-radius: 18px !important;
    border: 1px solid #cbd9c5 !important; background: #eaf3e6 !important;
    padding: 20px 28px !important; line-height: 1.65 !important;
    text-align: center !important;
    color: #344737 !important; -webkit-text-fill-color: #344737 !important;
    box-shadow: inset 0 1px 2px rgba(42, 59, 40, .035) !important;
}
#study-input,
#study-input .wrap,
.study-card .form,
.study-card .styler,
.study-card .block:not(.study-section-title) {
    background: transparent !important; color: #344737 !important;
}
.study-card .wrap { background: transparent !important; }
.study-card [role="combobox"] {
    color: #344737 !important; background: #eaf3e6 !important;
    border: 1px solid #cbd9c5 !important; border-radius: 16px !important;
}
#study-mode {
    box-sizing: border-box !important; width: min(100%, 280px) !important;
    min-width: 0 !important; margin: 18px auto 0 !important;
    padding: 0 !important;
}
#study-mode [data-testid="block-info"] {
    display: block; width: 100%; margin: 0 0 10px !important;
    padding: 0 !important; background: transparent !important;
    color: #53694f !important; text-align: center !important;
}
#study-mode label { text-align: center !important; }
#study-mode .secondary-wrap {
    border: 1px solid #91b08a !important; border-radius: 18px !important;
    background: #dcebd6 !important;
    box-shadow: 0 5px 14px rgba(53, 95, 67, .13) !important;
    transition: background-color .18s ease, box-shadow .18s ease, border-color .18s ease;
}
#study-mode .secondary-wrap:hover {
    background: #d2e5cb !important; border-color: #759a70 !important;
    box-shadow: 0 7px 18px rgba(53, 95, 67, .19) !important;
}
#study-mode .secondary-wrap:focus-within {
    border-color: #557d58 !important;
    box-shadow: 0 0 0 3px rgba(85, 125, 88, .2), 0 5px 14px rgba(53, 95, 67, .13) !important;
}
#study-mode [role="combobox"] {
    justify-content: center; text-align: center;
    background: transparent !important; border: 0 !important;
    box-shadow: none !important;
}
#study-mode [role="combobox"] input {
    box-sizing: border-box !important; width: 100% !important;
    min-width: 0 !important; text-align: center !important;
    background: transparent !important; border: 0 !important;
    box-shadow: none !important;
}
#study-mode .icon-wrap svg path { fill: #426b47 !important; }
#study-mode .icon-wrap { color: #426b47 !important; }
#study-input { border: 0 !important; padding: 0 !important; }
#study-input label { color: #53694f !important; background: transparent !important; }
#study-input label span {
    color: #53694f !important; background: transparent !important;
    box-sizing: border-box !important;
    display: block; width: 100%;
    padding: 0 clamp(8px, 1.5vw, 18px) !important;
    font-weight: 600;
}
#study-input textarea { margin-top: 8px; min-height: 190px; }
#study-input textarea:focus,
.study-card input:focus,
.study-card textarea:focus {
    border-color: #648662 !important;
    box-shadow: 0 0 0 3px rgba(100, 134, 98, .2) !important;
}
#study-send { margin-top: 18px; }
#study-send {
    min-height: 54px; border-radius: 18px !important;
    box-sizing: border-box !important; max-width: 100%; white-space: normal;
    background: #355f43 !important; border-color: #355f43 !important;
    color: #fffdf5 !important; font-weight: 650;
}
#study-send:hover { background: #294d36 !important; }
.study-note { color: #52634f !important; font-size: .92rem; line-height: 1.7; }
#study-buddy input::placeholder,
#study-buddy textarea::placeholder {
    color: #8a9284 !important; opacity: 1; text-align: center;
}
#study-answer {
    min-height: 250px; padding: 24px 30px !important;
    border: 1px solid #dce7d6; border-radius: 20px; background: #f2f7ef;
}
#study-answer .prose { color: #26382d; }
.study-card .wrap,
.study-card .form,
.study-card .block { border-radius: 18px; }
footer { display: none !important; }

@media (max-width: 820px) {
    #study-buddy .row { flex-direction: column !important; gap: 4px !important; }
    #study-buddy .column {
        box-sizing: border-box !important; width: 100% !important;
        min-width: 0 !important; flex: 1 1 100% !important;
    }
    #study-buddy .study-card { width: 100%; min-width: 0; }
    #study-buddy .study-card .prose { max-width: 100%; }
}

@media (max-width: 640px) {
    #study-buddy { padding: 14px 10px 24px; }
    #study-header { border-radius: 22px; padding: 26px 22px; }
    #study-header h1 { font-size: 1.55rem; }
    .study-card {
        box-sizing: border-box !important; min-width: 0 !important;
        border-radius: 22px !important; padding: clamp(12px, 4.8vw, 19px) !important;
    }
    #study-input textarea {
        min-height: 160px; padding: 18px clamp(10px, 5vw, 22px) !important;
    }
}

@media (max-width: 360px) {
    .gradio-container .contain { padding-left: 12px !important; padding-right: 12px !important; }
    #study-buddy { padding-left: 6px; padding-right: 6px; }
    .study-card { padding: 12px !important; }
    .study-card .study-card { padding: 0 !important; }
    #study-mode { width: 100% !important; }
    #study-mode .container,
    #study-mode .wrap,
    #study-mode .wrap-inner,
    #study-mode .secondary-wrap { box-sizing: border-box !important; min-width: 0 !important; }
    #study-mode .wrap-inner { padding-left: 4px !important; padding-right: 4px !important; }
    #study-mode [role="combobox"] { padding-left: 8px !important; padding-right: 8px !important; }
    #study-input textarea { padding-left: 10px !important; padding-right: 10px !important; }
}
"""


def _respond(prompt: str, study_mode: str) -> str:
    """Delegate the study request to the application service."""
    if not prompt or not prompt.strip():
        return "Add a question or some study material above to get started."
    return generate_study_response(prompt, study_mode)


def build_ui() -> gr.Blocks:
    """
    Constructs the Gradio web interface.
    
    Architectural Principle: The UI communicates strictly with `generate_response()`
    in the AI service layer and never directly with Ollama or the model client.
    """
    with gr.Blocks(
        title="StudyBuddy AI | Your study space",
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
                    gr.Markdown(
                        "### Your study toolkit",
                        elem_classes=["study-section-title"],
                    )
                    gr.Markdown(
                        "Choose a way to work with your material. Ask a question, "
                        "paste in notes, or try a practice activity.",
                        elem_classes=["study-note"],
                    )
                    study_mode = gr.Dropdown(
                        elem_id="study-mode",
                        choices=list(STUDY_MODES),
                        value="Study chat",
                        label="Study mode",
                        interactive=True,
                    )

                with gr.Group(elem_classes=["study-card"]):
                    gr.Markdown("### 📚 Course library")
                    gr.Markdown(
                        "Paste your course notes or a passage into the study box. "
                        "The selected model runs locally through Ollama; this version "
                        "does not store or retrieve uploaded course files.",
                        elem_classes=["study-note"],
                    )
                    gr.Markdown(
                        "**Tip:** Include the relevant notes for grounded answers.",
                        elem_classes=["study-note"],
                    )

            with gr.Column(scale=2, min_width=420):
                with gr.Group(elem_classes=["study-card"]):
                    gr.Markdown(
                        "### What are you studying today?",
                        elem_classes=["study-section-title"],
                    )
                    user_input = gr.Textbox(
                        elem_id="study-input",
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
                    gr.Markdown(
                        "Responses are AI-generated study aids. Check important facts against your course materials.",
                        elem_classes=["study-note"],
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
