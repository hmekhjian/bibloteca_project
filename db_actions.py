import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models import Base, Book


class dbActions:
    def __init__(self, db_path="sqlite:///bibloteca.db"):
        # Initialising SQLalchemy
        url = db_path
        self.engine = sa.create_engine(url)
        self.Session = sessionmaker(bind=self.engine)

        # Create the table if it doesn't exist
        Base.metadata.create_all(self.engine)

    def add_book(self, title, author, pages, status="To Read"):
        with self.Session() as session:
            new_book = Book(title =title, author= author, pages= pages, status= status)

            session.add(new_book)
            session.commit()

    def remove_book(self, **kwargs):
        with self.Session() as session:
            if "id" in kwargs and "title" in kwargs:
                raise ValueError("Please provide either an ID or title, not both")
            elif "id" in kwargs:
                book_id = kwargs["id"]
                book = session.query(Book).get(book_id)
            elif "title" in kwargs:
                book_title = kwargs["title"]
                book = session.query(Book).filter_by(title=book_title)
            else:
                raise ValueError(
                    "Please provide an ID or title to identify the book to be removed"
                )

            if book:
                session.delete(book)
                session.commit()

            else:
                raise Exception(
                    f"No book found with the provided {'id' if 'id' in kwargs else 'title'}."
                )

    def update_book(self, book_id, **kwargs):
        with self.Session() as session:
            book = session.query(Book).get(book_id)
            if book:
                for attr, value in kwargs.items():
                    setattr(book, attr, value)
                session.commit()
            else:
                raise Exception(f"Specified book with {book_id} not found")
