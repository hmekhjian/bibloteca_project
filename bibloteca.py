from textual.app import App, ComposeResult
from textual.widgets import Footer, Header


class biblotecaApp(App):
    """
    Textual TUI for managing your reading and book library
    """


if __name__ == "__main__":
    app = biblotecaApp()
    app.run()
