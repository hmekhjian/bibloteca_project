import sqlite3
from typing import List
from model import book

conn = sqlite3.connect("library.db")
c = conn.cursor()

# c.execute(
#     """CREATE TABLE books (
#     id integer,
#     Title text,
#     Author text,
#     yearPublished integer,
#     Pages integer,
#     dateStarted text,
#     dateFinished text,
#     pagesRead integer,
#     Read integer)
#     """
# )

# c.execute("INSERT INTO books VALUES (1, 'Dune', 'Frank Herbert', 1958, 568, '2016/03/12', '2016/03/24', 568, 1)")


def add_book():
    c.execute("select count(*) FROM books")
    count = c.fetchone()[0]
    book.id = count if count else 0
    with conn:
        c.execute(
            "INSERT INTO books VALUES (:id, :Title, :Author, :yearPublished, :Pages, :dateStarted, :dateFinished, :pagesRead, :Read)",
            {
                "Title": book.Title,
                "Author": book.Author,
                "yearPublished": book.yearPublished,
                "Pages": book.Pages,
                "dateStarted": book.dateStarted,
                "dateFinished": book.dateFinished,
                "pagesRead": book.pagesRead,
                "Read": book.Read,
            },
        )






def get_all_books() -> List[book]:
    c.execute("select * from books")
    results = c.fetchall()
    bookList = []
    for result in results:
        bookList.append(book(*result))
    return bookList

