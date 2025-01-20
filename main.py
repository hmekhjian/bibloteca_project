from db_actions import dbActions
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Static, ListItem, ListView, Label, Footer
from textual.containers import Vertical
from models import Book, Tag


db_actions = dbActions()


class biblotecaApp(App):
    CSS_PATH = "layout.tcss"

    BINDINGS = [("d", "remove_book", "Remove highlighted book")]

    def compose(self) -> ComposeResult:
        with Vertical(id="sidebar"):
            yield Footer()
            yield ListView(
                ListItem(Label("All")),
                ListItem(Label("Reading")),
                ListItem(Label("To Read")),
                ListItem(Label("Read")),
            )

        yield DataTable()

    def load_and_populate_table(self):
        table = self.query_one(DataTable)
        table.clear()
        table.cursor_type = "row"
        table.zebra_stripes = True
        

        table_data = db_actions.list_books()
        table.add_rows(table_data)

    def action_remove_book(self):
        table = self.query_one(DataTable)
        if table.row_count > 0:
            try:
                row_key = table.cursor_row
                row_data = table.get_row_at(row_key)
                id_cell = row_data[0]

                print(id_cell)

                db_actions.remove_book(id=id_cell)
                self.load_and_populate_table()

            except Exception as e:
                self.log(f"Error removing book: {e}") 

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "id", "title", "author", "pages", "progress", "status", "rating", "tags"
        )
        self.load_and_populate_table()
        table = self.query_one(DataTable)
        table.focus()


if __name__ == "__main__":
    app = biblotecaApp()
    app.run()
