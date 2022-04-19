import typer
import datetime, json, os
from rich.console import Console
from rich.table import Table
from rich import box
from collections import namedtuple
from dataclasses import dataclass
from pprint import pprint
from model import book
from database import get_all_books, add_book, delete_book
import os

app = typer.Typer()


@app.command(short_help="List all books currently in your library")
def list():
    bookTable = Table(title="Personal Reading", show_lines=True, box=box.HORIZONTALS)

    bookTable.add_column("id", justify="left", style="yellow", no_wrap=True)
    bookTable.add_column("Title", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Author", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Year", justify="left", style="cyan")
    bookTable.add_column("Pages", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Date started", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Date finished", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Progress", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Read", justify="left", style="cyan", no_wrap=True)

    book_list = get_all_books()
    for i in range(len(book_list)):
        bookTable.add_row(
            str(book_list[i].id),
            book_list[i].Title,
            book_list[i].Author,
            str(book_list[i].year_published),
            str(book_list[i].Pages),
            str(book_list[i].date_started),
            str(book_list[i].date_finished),
            str(round((book_list[i].pages_read / book_list[i].Pages) * 100)) + "%",
            "+" if book_list[i].Read == 1 else "-",
        )

    os.system("cls" if os.name == "nt" else "clear")
    console = Console()
    console.print(bookTable)


@app.command(short_help="Adds a book to the library")
def add(title: str, date_started: str = typer.Argument("x"), date_finished: str=typer.Argument("x"), pages_read: int = typer.Argument(0), read: int = typer.Argument(1), category: str=typer.Argument('Reading')):
    add_book(title, date_started, date_finished, pages_read, read, category)
    list()




@app.command(short_help="Removes a book from the library")
def remove(id: int):
    typer.echo("Removing book")
    delete_book(int(id))
    list()


@app.command(short_help="Updates information of the book")
def update(book_index: int):
    typer.echo("Updating book")
    list()


@app.command(short_help="Mark a book complete")
def complete(book_index: int):
    typer.echo("Book is completed")
    list()


if __name__ == "__main__":
    app()
