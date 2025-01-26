from db_actions import dbActions
from textual.app import App, ComposeResult
from textual.widgets import (
    DataTable,
    Static,
    ListItem,
    ListView,
    Label,
    Footer,
    Button,
    Input,
    OptionList,
    Placeholder,
    RichLog,
)
from textual.widgets.option_list import Option, Separator
from textual.screen import Screen
from textual.containers import Vertical, VerticalGroup, Container, Center, Horizontal
from models import Book, Tag
from textual import log


db_actions = dbActions()


class Book_Edit(Screen):
    """A widget to edit book information"""

    pass


class Book_addition(Screen):
    """A widget for adding books"""

    BINDINGS = [("b", "app.pop_screen", "Go Back")]

    def compose(self) -> ComposeResult:
        with Container(id="book-addition-dialog"):
            with Center():
                yield Input(placeholder="Book title, Author or ISBN", id="book-search")
            with Center():
                yield OptionList(id="search-results")
            with Center():
                yield Button("Add Book", id="add-book-button")
            yield Footer()


class biblotecaApp(App):
    CSS_PATH = "layout.tcss"

    BINDINGS = [
        ("a", "push_screen('book_addition')", "Add Book"),
        ("d", "remove_book", "Remove highlighted book"),
    ]

    SCREENS = {"book_addition": Book_addition}

    def compose(self) -> ComposeResult:
        with Horizontal(id="body"):
            with Vertical(id="sidebar"):

                all_tag_count = db_actions.get_all_tags()
                tag_option_list = [tag[0] for tag in all_tag_count]
                # log(tag_option_list)

                yield OptionList(
                    "All",
                    "Reading",
                    "To Read",
                    "Read",
                    Separator(),
                    *tag_option_list,  # TODO Need to look into the unpack operator and learn it's uses
                )

            yield DataTable()
            with Vertical(id="book-info"):
                yield Placeholder(id="book-cover")
                yield RichLog(id="book-details")
            yield Footer()

    #  Datatable to list all the books in the db with the appropriate info
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

    def action_add_book(self):
        new_book_screen = Book_addition()
        self.query_one(ComposeResult).mount(new_book_screen)
        new_book_screen.scroll_visible()

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
