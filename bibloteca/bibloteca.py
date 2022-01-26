import datetime
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


def bookInput():
    Title = input("What is the title of the book? ")
    Author = input("Who is the Author of the book? ")
    yearPublsihed = int(input("When was the book published? "))
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

    return {
        "Title": Title,
        "Author": Author,
        "Year Published": yearPublsihed,
        "Pages": Pages,
        "Date started": dateStarted,
        "Date finished": dateFinished,
        "Pages read": pagesRead,
        "Read": Read,
    }



newBook = bookInput()
bookList.append(newBook)
