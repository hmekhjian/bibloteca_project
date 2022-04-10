import typer
import datetime, json, os
from rich.console import Console
from rich.table import Table
from collections import namedtuple
from dataclasses import dataclass
from pprint import pprint


# bookList = []
bookIndex = namedtuple("bookID", "bookObject")


@dataclass
class book:
    id: int
    Title: str
    Author: str
    yearPublished: int
    Pages: int
    dateStarted: datetime.datetime
    dateFinished: datetime.datetime
    pagesRead: int = 0
    Read: bool = False





bookList = {}
with open("book_database.json") as json_file:
    bookData = json.loads(json_file.read())
    for b in bookData:
        newBook = book(**b)
        bookList[newBook.id] = newBook


app = typer.Typer()


@app.command()
def list():
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
            str(bookList[f"{i}"].id),
            bookList[f"{i}"].Title,
            bookList[f"{i}"].Author,
            str(bookList[f"{i}"].yearPublished),
            str(bookList[f"{i}"].Pages),
            str(bookList[f"{i}"].dateStarted),
            str(bookList[f"{i}"].dateFinished),
            str(bookList[f"{i}"].pagesRead),
            str(bookList[f"{i}"].Read),
        )

    console = Console()
    console.print(bookTable)


@app.command()
def add():
    typer.echo("Deleting user: Hiro Hamada")


@app.command()
def remove():
    typer.echo("Deleting user: Hiro Hamada")


if __name__ == "__main__":
    app()
