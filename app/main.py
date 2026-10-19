from app.ui import build_ui
from app.ui import STUDY_CSS, STUDY_THEME, build_ui

def main() -> None:
    """Entry point script for launching the application."""
    demo = build_ui()
    demo.launch(theme=STUDY_THEME, css=STUDY_CSS)

if __name__ == "__main__":
    main()
