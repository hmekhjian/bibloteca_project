from textual.containers import Container
from textual.app import ComposeResult
from textual.widgets import DataTable, OptionList
from textual.widgets.option_list import Option, Separator
from db_actions import dbActions
from textual import work, on, log


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


# Sidebar Components
class FilterList(OptionList):
    def __init__(self):
        super().__init__()
        self.db_actions = dbActions()
        self.id = "filter-list"

    def on_mount(self) -> None:
        self.load_filters()

    def load_filters(self) -> None:
        self.add_options(["All", "Reading", "To Read", "Read"])


class TagList(OptionList):
    def __init__(self):
        super().__init__()
        self.db_actions = dbActions()
        self.id = "tag-list"

    async def on_mount(self):
        await self.load_tags()

    async def load_tags(self):
        all_tag_count = await self.db_actions.get_all_tags()
        tag_option_list = [tag[0] for tag in all_tag_count]
        log(tag_option_list)
        for tag in tag_option_list:
            self.add_option(Option(tag))


class Sidebar(Container, can_focus=True):
    BORDER_TITLE = "Filters"

    def compose(self) -> ComposeResult:
        yield FilterList()
        yield TagList()
