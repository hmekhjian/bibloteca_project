from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
import sqlalchemy as sa
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    Mapped,
    relationship,
    mapped_column,
)

# Initialising SQLalchemy
engine = sa.create_engine("sqlite:///bibloteca.db")

Session = sessionmaker(bind=engine)

Base = declarative_base()


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


Base.metadata.create_all(engine)

with Session() as session:
    book1 = Book(title="Dune", author="Frank Herber", pages=410, status="Read")

    session.add_all([book1])
    session.commit()

    # class biblotecaApp(App):
    """
    Textual TUI for managing your reading and book library
    """


# if __name__ == "__main__":
#     app = biblotecaApp()
#     app.run()
