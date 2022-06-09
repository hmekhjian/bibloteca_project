import sqlite3, requests
from typing import List
from model import book


conn = sqlite3.connect("library.db")
c = conn.cursor()

c.execute(
    """CREATE TABLE IF NOT EXISTS books (
    id integer,
    Title text,
    Author text,
    year_published integer,
    Pages integer,
    date_started text,
    date_finished text,
    pages_read integer,
    status text)
    """
)


def add_book(title, date_started, date_finished, pages_read, status):

    # Set the book.id based on the number of items in the database table
    c.execute("SELECT count(*) FROM books")
    count = c.fetchone()[0]
    book.id = count if count else 0

    # Search for the book title on OpenLibrary and pull the neccessary data from the json
    searchTerm = title.strip().replace(" ", "+")
    response = requests.get(
        f"http://openlibrary.org/search.json?q={searchTerm}&limit=1"
    )

    data = response.json()
    book.Title = data["docs"][0]["title"]
    book.Author = data["docs"][0]["author_name"][0]
    book.year_published = data["docs"][0]["first_publish_year"]
    book.Pages = int(data["docs"][0]["number_of_pages_median"])
    book.date_started = date_started
    book.date_finished = date_finished
    book.status = status

    # Set the number of pages_read based on the status of the book
    if book.status == "Completed":
        book.pages_read = book.Pages
    else:
        book.pages_read = pages_read

    # Write the book instance to the Sqlite table
    with conn:
        c.execute(
            "INSERT INTO books VALUES (:id, :Title, :Author, :year_published, :Pages, :date_started, :date_finished, :pages_read, :status)",
            {
                "id": book.id,
                "Title": book.Title,
                "Author": book.Author,
                "year_published": book.year_published,
                "Pages": book.Pages,
                "date_started": book.date_started,
                "date_finished": book.date_finished,
                "pages_read": book.pages_read,
                "status": book.status,
            },
        )


def delete_book(id):
    c.execute("SELECT count(*) FROM books")
    count = c.fetchone()[0]

    with conn:
        c.execute(f"DELETE FROM books WHERE id = :id", {"id": id})
        # Reposition the book.id
        for pos in range(id+1, count):
            change_id(pos, pos-1, False)

# Function for renumbering the book.id
def change_id(old_id: int, new_id: int, commit = True):
    c.execute('UPDATE books SET id = :new_id WHERE id = :old_id', {'old_id': old_id, 'new_id': new_id})
    if commit:
        conn.commit()



def get_all_books(list_order) -> List[book]:
    c.execute(f"select * from books {list_order}")
    results = c.fetchall()
    bookList = []
    for result in results:
        bookList.append(book(*result))
    return bookList


def complete_book(id):
    c.execute("SELECT count(*) FROM books")
    count = c.fetchone()[0]

    with conn:
        c.execute(f"UPDATE books SET Pages = :new_page WHERE id = :id", {"new_page": id})
        # Reposition the book.id
        for pos in range(id+1, count):
            change_id(pos, pos-1, False)