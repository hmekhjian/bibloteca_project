from textual.containers import Container
from textual.app import ComposeResult
from textual.widgets import DataTable
from db_actions import dbActions
from textual import work, on


class ResultsTable(DataTable, inherit_bindings=False):
    DEFAULT_CSS = """
        .Book_results {
            height: 100%
            width: 100%}
        """

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.db_actions = dbActions()
        self.add_class("Book_results")

    def on_mount(self) -> None:
        self.add_columns(
            "id", "title", "author", "pages", "progress", "status", "rating", "tags"
        )
        self.load_table()

    #  Datatable to list all the books in the db with the appropriate info
    @work(exclusive=True)
    async def load_table(self):
        self.clear()
        self.cursor_type = "row"
        self.zebra_stripes = True

        table_data = await self.db_actions.list_books()
        self.add_rows(table_data)


class ResultsViewer(Container, can_focus=True, id="results-viewer"):
    BORDER_TITLE = "Book Results"

    def compose(self) -> ComposeResult:
        yield ResultsTable()

    def on_mount(self, event):
        self.query_one(ResultsTable).focus()
