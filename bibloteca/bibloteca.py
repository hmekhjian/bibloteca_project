import datetime
from dataclasses import dataclass


bookList = []


@dataclass
class book:
    ID: int
    Title: str
    Author: str
    yearPublished: int
    Pages: int
    dateStarted: datetime.datetime
    dateFinished: datetime.datetime
    pagesRead: int = 0
    Read: bool = False


def bookInput():

    Title = input("What is the title of the book? ")
    Author = input("Who is the Author of the book? ")
    yearPublsihed = int(input("When was the book published? "))
    Pages = int(input("How long is the book? "))
    dateStarted = datetime.datetime.strptime(
        str(input("When did you start reading the book? (yyyy-mm-dd) ")), "%Y-%m-%d"
    )

    # Check the book has been finished
    readCheck = input("Have you finished the book? [Y/N] ")
    if readCheck == "Y":
        Read = True
    else:
        Read = False

    # If the book has been finished ask for the finish date
    if Read == "True":
        dateFinished = datetime.strptime(
            str(input("When did you finish reading the book? (yyyy-mm-dd) ")),
            "%Y-%m-%d",
        )

        pagesRead = Pages

    else:
        pagesRead = int(input("How many pages have you read? "))
        dateFinished = None

    return (
        Title,
        Author,
        yearPublsihed,
        Pages,
        dateStarted,
        dateFinished,
        pagesRead,
        Read,
    )


def addBook(bookInfo):
    newBook = book
    newBook.Title = Title
    newBook.Author = Author
    newBook.yearPublished = yearPubslished
    newBook.Pages = Pages
    newBook.pagesRead = pagesRead
    newBook.dateStarted = dateStarted
    newBook.dateFinished = dateFinished
    newBook.Read = Read

    bookList.append(newBook)


bookInfo = bookInput()
addBook(bookInfo)

print(bookList)

