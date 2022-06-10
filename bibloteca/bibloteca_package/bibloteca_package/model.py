from dataclasses import dataclass
import datetime


@dataclass
class book:
    id: int
    Title: str
    Author: str
    year_published: int
    Pages: int
    date_started: str  # datetime.datetime
    date_finished: str  # datetime.datetime
    pages_read: int = 0
    status: str = "Reading"