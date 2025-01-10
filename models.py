import typing
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
import sqlalchemy as sa

Base = declarative_base()  # Create Base here

# Setup classes for the book objects


class Book(Base):
    __tablename__ = "Books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    pages: Mapped[int]
    rating: Mapped[float] = mapped_column(default=0.0)
    status: Mapped[str] = mapped_column(default="To Read")
    progress: Mapped[int] = mapped_column(default=0)
    # tags: Mapped[list]

    allowed_status = ["To Read", "Read", "Reading"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.status not in self.allowed_status:
            raise ValueError(
                "The only allowed status values are 'To Read', 'Reading', and 'Read'"
            )

        if self.status == "Read":
            self.progress = self.pages

    def __repr__(self):
        return (f"Book(id={self.id}, title={self.title}, author={self.author}, "
                f"pages={self.pages}, rating={self.rating}, status={self.status}, "
                f"progress={self.progress})")

    def update_rating(self, rating):
        self.rating = rating
        return self

    def update_status(self, status):
        self.status = status
        return self

    def update_progress(self, progress):
        self.progress = progress
        return self
