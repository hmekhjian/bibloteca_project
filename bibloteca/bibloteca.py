import datetime, json

from rich.console import Console
from rich.table import Table

from types import SimpleNamespace
from dataclasses import dataclass, field
from itertools import count


bookList = []


@dataclass
class book:
    id: int = field(default_factory=count().__next__, init=False)
    Title: str
    Author: str
    yearPublished: int
    Pages: int
    dateStarted: datetime.datetime
    dateFinished: datetime.datetime
    pagesRead: int = 0
    Read: bool = False


def addBook():
    Title = input("What is the title of the book? ")
    Author = input("Who is the Author of the book? ")
    yearPublished = int(input("When was the book published? "))
    Pages = int(input("How long is the book? "))
    dateStarted = datetime.datetime.strptime(
        str(input("When did you start reading the book? (yyyy-mm-dd) ")), "%Y-%m-%d"
    )

    # Check the book has been finished and ff the book has been finished ask for the finish date
    readCheck = input("Have you finished the book? [Y/N] ")
    if readCheck == "Y":
        Read = True
        dateFinished = datetime.datetime.strptime(
            str(input("When did you finish reading the book? (yyyy-mm-dd) ")),
            "%Y-%m-%d",
        )
        pagesRead = Pages
    else:
        Read = False
        pagesRead = int(input("How many pages have you read? "))
        dateFinished = None

    bookInstance = book(
        Title, Author, yearPublished, Pages, dateStarted, dateFinished, pagesRead, Read
    )

    bookList.append(bookInstance)


def removeBook(id):
    for i in range(len(bookList)):
        if bookList[i].id == id:
            del bookList[i]


def listBooks():

    bookTable = Table(title="Personal Reading")

    bookTable.add_column("id", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Title", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Author", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Year", justify="left", style="cyan")
    bookTable.add_column("Pages", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Date started", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Date finished", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Progress", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Read", justify="left", style="cyan", no_wrap=True)

    for i in range(len(bookList)):
        bookTable.add_row(
            str(bookList[i].id),
            bookList[i].Title,
            bookList[i].Author,
            str(bookList[i].yearPublished),
            str(bookList[i].Pages),
            str(bookList[i].dateStarted),
            str(bookList[i].dateFinished),
            str(bookList[i].pagesRead),
            str(bookList[i].Read),
        )

    console = Console()
    console.print(bookTable)


with open("book_database.json") as f:
    bookData = json.load(f, object_hook=lambda d: SimpleNamespace(**d))


# listBooks()
