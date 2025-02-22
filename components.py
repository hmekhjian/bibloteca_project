from textual.containers import Container
from textual.widgets import DataTable, Static, OptionList
from main import db_actions


class resultsTable(DataTable, inherit_bindings=False, id="results_table"):
    DEFAULT_CSS = """
        Book_results {
            height: 100%
            width: 100%}
        """

    def on_mount(self) -> None:
        self.add_columns(
            "id", "title", "author", "pages", "progress", "status", "rating", "tags"
        )

    #  Datatable to list all the books in the db with the appropriate info
    def load_table(self):
        table = self
        table.clear()
        table.cursor_type = "row"
        table.zebra_stripes = True

        table_data = db_actions.list_books()
        table.add_rows(table_data)


class resultsViewer(Container, can_focus=True, id="results-viewer"):
    BORDER_TITLE = "Book Results"

    def on_mount(self, event):
        results = self.query_one(resultsTable)
        results.load_table()
        results.focus()
