from textual.containers import Container
from textual.app import ComposeResult
from textual.widgets import DataTable
from db_actions import dbActions
from textual import work, on


class ResultsTable(DataTable):
    DEFAULT_CSS = """
        .Book_results {
            height: 100%;
            width: 100%;}
        """

    def __init__(self):
        super().__init__()
        self.db_actions = dbActions()

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

        table_data = await self.db_actions.list_books()
        self.add_rows(table_data)


class ResultsViewer(Container, can_focus=True):
    BORDER_TITLE = "Book Results"

    def compose(self) -> ComposeResult:
        yield ResultsTable()

    def on_mount(self, event):
        self.query_one(ResultsTable).focus()
