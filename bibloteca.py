from db_actions import dbActions
db_actions = dbActions()
books_data = [
    {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "pages": 224,
        "status": "Read",
        "tag_names": ["sci-fi", "comedy", "classic"],
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "pages": 432,
        "status": "To Read",
        "tag_names": ["classic", "romance", "fiction"],
    },
    {
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "pages": 1216,
        "status": "Reading",
        "tag_names": ["fantasy", "classic", "adventure"],
    },
    {
        "title": "The Book Thief",
        "author": "Markus Zusak",
        "pages": 552,
        "status": "Read",
        "tag_names": ["historical fiction", "war", "young adult"],
    },
    {
        "title": "The Martian",
        "author": "Andy Weir",
        "pages": 384,
        "status": "Read",
        "tag_names": ["sci-fi", "survival", "adventure"],
    },
]

# Add the sample data to the database
for book_data in books_data:
    db_actions.add_book(**book_data)
