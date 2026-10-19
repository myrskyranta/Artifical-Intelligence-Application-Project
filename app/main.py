from app.ui import build_ui, ui_launch_options

def main() -> None:
    """Entry point script for launching the application."""
    demo = build_ui()
    demo.launch(**ui_launch_options())

if __name__ == "__main__":
    main()
