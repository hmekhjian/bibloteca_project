import typer
import datetime, json, os
from rich.console import Console
from rich.table import Table
from collections import namedtuple
from dataclasses import dataclass
from pprint import pprint
from model import book
from database import get_all_books

app = typer.Typer()




@app.command(short_help="List all books currently in your library")
def list():
    bookTable = Table(title="Personal Reading")

    bookTable.add_column("id", justify="left", style="yellow", no_wrap=True)
    bookTable.add_column("Title", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Author", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Year", justify="left", style="cyan")
    bookTable.add_column("Pages", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Date started", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Date finished", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Progress", justify="left", style="cyan", no_wrap=True)
    bookTable.add_column("Read", justify="left", style="cyan", no_wrap=True)


    bookList = get_all_books()
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
            '+' if bookList[i].Read == 1 else '-')
            

    console = Console()
    console.print(bookTable)


@app.command(short_help="Adds a book to the library")
def add(title: str):
    typer.echo(f"Adding '{title}' to the library")
    list()


@app.command(short_help="Removes a book from the library")
def remove(bookIndex: int):
    typer.echo("Removing book")
    list()


@app.command(short_help="Updates information of the book")
def update(bookIndex: int):
    typer.echo("Updating book")
    list()


@app.command(short_help="Mark a book complete")
def complete(bookIndex: int):
    typer.echo("Book is completed")
    list()






if __name__ == "__main__":
    app()
