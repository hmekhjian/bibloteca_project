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
from textual import log, on, work
from textual.reactive import reactive
from textual.message import Message
import book_api
from typing import Optional, Dict, Any

db_actions = dbActions()


class Book_Edit(Screen):
    """A widget to edit book information"""

    pass


class Book_addition(Screen):
    """A widget for adding books"""

    BINDINGS = [("b", "app.pop_screen", "Go Back")]

    results = reactive([])

    class BookAdded(Message):
        def __init__(self) -> None:
            super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id="book-addition-dialog"):
            with Center():
                yield Input(placeholder="Book title, Author or ISBN", id="book-search")
            with Center():
                self.search_results = OptionList(id="search-results")
                yield self.search_results
            with Center():
                yield Button("Add Book", id="add-book-button")
            yield Footer()

    @on(Input.Submitted, "#book-search")
    async def search_books(self, event: Input.Submitted):
        search_term = book_api.safe_search_term(event.value)

        if search_term:
            self.search_results.clear_options()
            self.search_results.add_option(Option("Searching..."))
            self.api_search(search_term)

        else:
            self.search_results.clear_options()
            self.search_results.add_option(Option("Nothing Found :("))

    @work(exclusive=True)
    async def api_search(self, search_term):
        try:
            self.results = await book_api.search_book(book_api.api_key, search_term, 5)

            if self.results != None:
                options = [
                    Option(f"{item["volumeInfo"]["title"]} ")
                    for item in self.results["items"]
                ]
                self.show_results(options)
            else:
                self.show_results([Option("No Results Found", disabled=True)])

        except Exception as e:
            self.show_results([Option(f"Error: {e}")])

    def show_results(self, options: list[Option]):
        self.search_results.clear_options()
        for option in options:
            self.search_results.add_option(option)

    @on(OptionList.OptionSelected, "#search-results")
    def select_book(self):
        i = self.search_results.highlighted
        selected_title = self.results["items"][i]["volumeInfo"]["title"]
        selected_author = self.results["items"][i]["volumeInfo"]["authors"][0]
        selected_pages = self.results["items"][i]["volumeInfo"]["pageCount"]
        log(selected_author, selected_title, selected_pages)
        db_actions.add_book(selected_title, selected_author, selected_pages)
        self.post_message(self.BookAdded())
        app.pop_screen()


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

                self.status_filter_list = OptionList(
                    Option("All"),
                    Option("Reading"),
                    Option("To Read"),
                    Option("Read"),
                )
                self.status_filter_list.border_title = "Status Filter"
                yield self.status_filter_list

                self.tag_filter_list = OptionList(
                    *tag_option_list,
                    id="filter-list",
                )
                self.tag_filter_list.border_title = "Tag Filter"
                yield self.tag_filter_list
            with Container():
                self.book_list = DataTable(id="book-list")
                self.book_list.border_title = "Book Results"
                yield self.book_list
            with Vertical(id="book-info"):
                yield Placeholder(id="book-cover")
                yield RichLog(id="book-details")
            yield Footer()

    @on(OptionList.OptionHighlighted, "#status-filter-list")
    def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted):
        status_list = ["Reading", "To Read", "Read"]
        if event.option is not None:
            if event.option.prompt == "All":
                self.load_and_populate_table()
            elif event.option.prompt in status_list:
                table = self.query_one(DataTable)
                table.clear()
                table_data = db_actions.get_books_by_status(event.option.prompt)
                table.add_rows(table_data)
            else:
                table = self.query_one(DataTable)
                table.clear()
                table_data = db_actions.get_books_by_tag(event.option.prompt)
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

    @on(Book_addition.BookAdded)
    def on_book_added(self, event: Book_addition.BookAdded):
        self.load_and_populate_table()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(
            "id", "title", "author", "pages", "progress", "status", "rating", "tags"
        )
        self.load_and_populate_table()
        table.focus()


if __name__ == "__main__":
    app = biblotecaApp()
    app.run()
