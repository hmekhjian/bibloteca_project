from db_actions import dbActions
from textual.app import App, ComposeResult
from textual.widgets import DataTable
from models import Book, Tag


db_actions = dbActions()


class biblotecaApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns(
            "id", "title", "author", "pages", "progress", "status", "rating", "tags"
        )

        table_data = db_actions.list_books()
        table.add_rows(table_data)


if __name__ == "__main__":
    app = biblotecaApp()
    app.run()
