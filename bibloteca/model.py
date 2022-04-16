from dataclasses import dataclass
import datetime


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
