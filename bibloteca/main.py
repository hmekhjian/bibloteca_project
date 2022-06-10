import typer
import datetime, json, os
from rich.text import Text
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
def list(order: bool = typer.Option(False)):
    if order:
        list_order = 'ORDER BY status'
    else:
        list_order = ''
    bookTable = Table(title="Personal Library", show_lines=True, box=box.HORIZONTALS)

    bookTable.add_column("id", justify="left", style="grey85", no_wrap=True)
    bookTable.add_column("Title", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Author", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Year", justify="left", style="cyan")
    bookTable.add_column("Pages", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Progress", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Status", justify="left", style="cyan", no_wrap=True)

    book_list = get_all_books(list_order)

    for i in range(len(book_list)):
        # Set colour for status rows
        if book_list[i].status == 'Completed':
            status_color = 'green'
        elif book_list[i].status == 'Want to read':
            status_color = 'yellow'
        elif book_list[i].status == 'Reading':
            status_color = 'blue'
        # Generate each row
        bookTable.add_row(
            str(book_list[i].id),
            book_list[i].Title,
            book_list[i].Author,
            str(book_list[i].year_published),
            str(book_list[i].Pages),
            str(round((book_list[i].pages_read / book_list[i].Pages) * 100)) + "%",
            Text().append(book_list[i].status, style=f"bold {status_color}")
        )
    
    os.system("cls" if os.name == "nt" else "clear")
    console = Console()
    console.print(bookTable)


@app.command(short_help="Adds a book to the library")
def add(
    title: str,
    date_started: str = typer.Argument("x"),
    date_finished: str = typer.Argument("x"),
    # pages_read: int = typer.Argument(0),
    reading: bool = typer.Option(
        False, show_default=False, help="Set the status to reading"
    ),
    toread: bool = typer.Option(
        False, show_default=False, help="Set the status to Want to read"
    ),
    completed: bool = typer.Option(
        False, show_default=False, help="Set the status to completed"
    ),
    progress: int = typer.Option(
        0, show_default=False, help="Set the numer of pages read"
    ),
):
    status = "Completed"
    pages_read = progress
    if reading:
        status = "Reading"
    elif toread:
        status = "Want to read"
    elif completed:
        status = "Completed"

    add_book(title, date_started, date_finished, pages_read, status)
    list('')


@app.command(short_help="Removes a book from the library")
def remove(id: int):
    typer.echo("Removing book")
    delete_book(int(id))
    list('')


@app.command(short_help="Updates book progress")
def update(book_index: int):
    typer.echo("Updating book progress")
    list()


@app.command(short_help="Mark a book complete")
def complete(book_index: int):
    typer.echo("Book is completed")
    list()


if __name__ == "__main__":
    app()
