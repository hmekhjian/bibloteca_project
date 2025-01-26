import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Book, Tag, book_tag_table
from contextlib import contextmanager


class dbActions:
    def __init__(self, db_path="sqlite:///bibloteca.db"):
        # Initialising SQLalchemy
        url = db_path
        self.engine = sa.create_engine(url)
        self.Session = sessionmaker(bind=self.engine)

        # Create the table if it doesn't exist
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_factory(self):
        session = self.Session()

        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    # TODO Refactor all queries to use sa.select method. statmenet => excecute
    def get_book_by_id(self, id, session):
        book = session.query(Book).get(id)
        return book

    def get_book_by_title(self, title):
        with self.session_factory() as session:
            book = session.query(Book).filter_by(title=title)
            return book

    # Add add ordering for sorting options in the app and custom filtering for use with tags later on
    def list_books(self):
        with self.session_factory() as session:
            stmt = sa.select(Book).options(joinedload(Book.tags))
            result = session.execute(stmt)
            book_list = result.scalars().unique().all()
            book_details = []
            for book in book_list:
                book_details.append(
                    (
                        book.id,
                        book.title,
                        book.author,
                        book.pages,
                        book.progress,
                        book.status,
                        f"⭐ {book.rating}",
                        ", ".join([tag.name for tag in book.tags]),
                    )
                )
            return book_details

    def add_book(self, title, author, pages, status="To Read", tag_names=None):
        with self.session_factory() as session:
            new_book = Book(title=title, author=author, pages=pages, status=status)

            if tag_names:
                tag_query = sa.select(Tag).where(Tag.name.in_(tag_names))
                existing_tags = session.execute(tag_query).scalars().all()
                existing_tag_names = {tag.name for tag in existing_tags}
                for tag_name in tag_names:
                    if tag_name in existing_tag_names:
                        new_book.tags.append(
                            next(tag for tag in existing_tags if tag.name == tag_name)
                        )
                    else:
                        new_tag = Tag(name=tag_name)
                        session.add(new_tag)
                        new_book.tags.append(new_tag)

            session.add(new_book)

    def remove_book(self, **kwargs):
        with self.session_factory() as session:
            if "id" in kwargs and "title" in kwargs:
                raise ValueError("Please provide either an ID or title, not both")
            elif "id" in kwargs:
                book_id = kwargs["id"]
                book = self.get_book_by_id(book_id, session)
            elif "title" in kwargs:
                book_title = kwargs["title"]
                book = self.get_book_by_title(book_title, session)
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

    def add_book_tag(self, book_id, tags):

        with self.session_factory() as session:
            if not tags:
                raise ValueError("Please provide a valid tag or tags.")
            tag_names = [tags] if isinstance(tags, str) else tags
            book = self.get_book_by_id(book_id, session)

            if not book:
                raise ValueError(f"No book with the ID {book_id} was found")

            tag_query = sa.select(Tag).where(Tag.name.in_(tag_names))
            existing_tags = session.execute(tag_query).scalars().all()
            existing_tag_names = {tag.name for tag in existing_tags}
            for tag_name in tags:
                if tag_name in existing_tag_names:
                    book.tags.append(
                        next(tag for tag in existing_tags if tag.name == tag_name)
                    )
                else:
                    new_tag = Tag(name=tag_name)
                    session.add(new_tag)
                    book.tags.append(new_tag)

    # TODO Add a remove tag from book function and think about what happens to tags if book with a tag are deleted. Are they orphaned and kept i nthe dp or cleaned up?

    def get_all_tags(self):
        with self.session_factory() as session:
            stmt = (
                sa.select(
                    Tag.name, sa.func.count(book_tag_table.c.book_id).label("tag_count")
                )
                .join(book_tag_table, Tag.id == book_tag_table.c.book_id, isouter=True)
                .group_by(Tag.name)
                .order_by(sa.desc("tag_count"))
            )

            result = session.execute(stmt).all()
            return [row for row in result]
