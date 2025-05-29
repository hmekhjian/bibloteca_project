import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Book, Tag, book_tag_table
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import List, Tuple, Optional
from sqlalchemy import select
import asyncio


class dbActions:
    def __init__(self, db_path="sqlite+aiosqlite:///bibloteca.db"):
        # Initialising SQLalchemy
        self.db_url = db_path
        self.engine = create_async_engine(self.db_url, echo=False)
        self.async_session_facotry = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )

    # Create the table if it doesn't exist
    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session_factory(self):
        session: AsyncSession = self.async_session_facotry()

        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def get_book_by_id(self, book_id):
        async with self.session_factory() as session:
            stmt = select(Book).where(Book.id == book_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_book_by_title(self, title):
        async with self.session_factory() as session:
            stmt = select(Book).where(Book.title == title)
            result = await session.execute(stmt)
            return result.scalars().all()

    # Add add ordering for sorting options in the app and custom filtering for use with tags later on
    async def list_books(self) -> List[Tuple]:
        try:
            async with self.session_factory() as session:
                stmt = sa.select(Book).options(joinedload(Book.tags))
                result = await session.execute(stmt)
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
        except Exception as e:
            print(f"Database error: {e}")
            return []

    async def add_book(self, title, author, pages, status="To Read", tag_names=None):
        async with self.session_factory() as session:
            new_book = Book(title=title, author=author, pages=pages, status=status)

            if tag_names:
                tag_query = sa.select(Tag).where(Tag.name.in_(tag_names))
                existing_tags = await session.execute(tag_query).scalars().all()
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

    async def remove_book(self, **kwargs):
        async with self.session_factory() as session:
            if "id" in kwargs and "title" in kwargs:
                raise ValueError("Please provide either an ID or title, not both")
            elif "id" in kwargs:
                book_id = kwargs["id"]
                book = await self.get_book_by_id(book_id)
            elif "title" in kwargs:
                book_title = kwargs["title"]
                book = self.get_book_by_title(book_title)
            else:
                raise ValueError(
                    "Please provide an ID or title to identify the book to be removed"
                )

            if book:
                await session.delete(book)

            else:
                raise Exception(
                    f"No book found with the provided {'id' if 'id' in kwargs else 'title'}."
                )

    async def update_book(self, book_id, **kwargs):
        async with self.session_factory() as session:
            book = await self.get_book_by_id(book_id)
            if book:
                for attr, value in kwargs.items():
                    setattr(book, attr, value)
                session.add(book)
            else:
                raise Exception(f"Specified book with {book_id} not found")

    async def add_book_tag(self, book_id, tags):

        async with self.session_factory() as session:
            if not tags:
                raise ValueError("Please provide a valid tag or tags.")
            tag_names = [tags] if isinstance(tags, str) else tags
            book = await self.get_book_by_id(book_id)

            if not book:
                raise ValueError(f"No book with the ID {book_id} was found")

            tag_query = sa.select(Tag).where(Tag.name.in_(tag_names))
            existing_tags = await session.execute(tag_query).scalars().all()
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

    async def get_all_tags(self):
        async with self.session_factory() as session:
            stmt = (
                sa.select(
                    Tag.name, sa.func.count(book_tag_table.c.book_id).label("tag_count")
                )
                .join(book_tag_table, Tag.id == book_tag_table.c.book_id, isouter=True)
                .group_by(Tag.name)
                .order_by(sa.desc("tag_count"))
            )

            result = await session.execute(stmt)
            return [row for row in result.all()]

    # TODO Create helper function to convert book objects to a list of tuples for both functions below to reduce repetition
    async def get_books_by_tag(self, tag_name):
        async with self.session_factory() as session:
            stmt = (
                sa.select(Book)
                .join(Book.tags)
                .where(Tag.name == tag_name)
                .options(joinedload(Book.tags))
            )

            results = await session.execute(stmt)
            book_list = results.scalars().unique().all()
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

    async def get_books_by_status(self, status):
        async with self.session_factory() as session:
            stmt = (
                sa.select(Book)
                .where(Book.status == status)
                .options(joinedload(Book.tags))
            )

            results = await session.execute(stmt)
            book_list = results.scalars().unique().all()
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

    async def close(self):
        if self.engine:
            await self.engine.dispose()
