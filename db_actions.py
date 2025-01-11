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

    def get_book_by_id(self, id):
        with self.Session() as session:
            book = session.query(Book).get(id)
            return book

    def get_book_by_title(self, title):
        with self.Session() as session:
            book = session.query(Book).filter_by(title=title)
            return book

    # Add add ordering for sorting options in the app and custom filtering for use with tags later on
    def list_books(self):
        with self.Session() as session:
            book_list = session.query(Book).all()
            return book_list

    def add_book(self, title, author, pages, status="To Read"):
        with self.Session() as session:
            new_book = Book(title=title, author=author, pages=pages, status=status)

            session.add(new_book)
            session.commit()

    def remove_book(self, **kwargs):
        with self.Session() as session:
            if "id" in kwargs and "title" in kwargs:
                raise ValueError("Please provide either an ID or title, not both")
            elif "id" in kwargs:
                book_id = kwargs["id"]
                book = self.get_book_by_id(book_id)
            elif "title" in kwargs:
                book_title = kwargs["title"]
                book = self.get_book_by_title(book_title)
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
            book = self.get_book_by_id(book_id)
            if book:
                for attr, value in kwargs.items():
                    method_name = f"update_{attr}"
                    if hasattr(book, method_name):
                        update_method = getattr(book, method_name)
                        update_method(value)
                        session.add(book)
                session.commit()
            else:
                raise Exception(f"Specified book with {book_id} not found")
