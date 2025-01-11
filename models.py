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

    #  TODO Add the many to many relationship to the database to create tag functionality

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
        return (
            f"Book(id={self.id}, title={self.title}, author={self.author}, "
            f"pages={self.pages}, rating={self.rating}, status={self.status}, "
            f"progress={self.progress})"
        )

    def update_rating(self, new_rating: float):
        if isinstance(new_rating, float) and 0 <= new_rating <= 5.0:
            self.rating = new_rating
            return self
        else:
            raise ValueError(
                f"{new_rating} is not a valid rating. Please provide a rating between 0 and 5.0 as a floating point number"
            )

    def update_status(self, status: str):
        if status not in self.allowed_status:
            self.status = status
            return self
        else:
            raise ValueError(
                "The only allowed status values are 'To Read', 'Reading', and 'Read'"
            )

    def update_progress(self, new_progress: int):
        if isinstance(new_progress, int) and 0 <= new_progress <= self.pages:
            self.progress = new_progress
            return self
        else:
            raise ValueError(
                f"{new_progress} is not a valid value for progress. Please enter a number between 0 and {self.pages}"
            )
