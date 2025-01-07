import typing
from bibloteca import Base

# Setup classes for the book objects


class Book(Base):
    allowed_status = ["To Read", "Read", "Reading"]

    def __init__(
        self, title, author, pages, rating = 0.0 , status="To Read", progress=0, tags = None
    ):
        self.title = title
        self.author = author
        self.pages = pages
        self.tags = tags if tags is not None else []

        if status in Book.allowed_status:
            self.status = status
        else:
            raise ValueError(
                "The only allowed status values are 'To Read', 'Reading', and 'Read'"
            )
        if self.status == "Read":
            self.progress = self.pages
        else:
            self.progress = progress

        self.rating = rating

    def __repr__(self):
        return f"title: {self.title}\nauthor: {self.author}\npages: {self.pages}\nprogress: {self.progress}"

    def add_tag(self, new_tag):
        self.tags.append(new_tag)
    
    def remove_tag(self, tag):
        self.tags.remove(tag)

    def update_progress(self, new_progress):
        self.progress = new_progress
        if self.get_progress_percentage(self) == 100:
            self.status = "Read"
        return self

    def update_rating(self, new_rating):
        self.rating = new_rating

    def set_status(self, new_status):
        self.status = new_status

    def get_progress_percentage(self):
        if self.progress == 0:
            return 0
        return self.progress / self.pages * 100


book = Book("Dune", "Frank Herbert", 412)
print(book)
