from db_actions import dbActions
import asyncio


async def main():
    db_actions = dbActions()

    books = await db_actions.get_books_by_tag("war")
    print(books)


if __name__ == "__main__":
    asyncio.run(main())


# books_data = [
#     {
#         "title": "the hitchhiker's guide to the galaxy",
#         "author": "douglas adams",
#         "pages": 224,
#         "status": "read",
#         "tag_names": ["sci-fi", "comedy", "classic"],
#     },
#     {
#         "title": "pride and prejudice",
#         "author": "jane austen",
#         "pages": 432,
#         "status": "to read",
#         "tag_names": ["classic", "romance", "fiction"],
#     },
#     {
#         "title": "the lord of the rings",
#         "author": "j.r.r. tolkien",
#         "pages": 1216,
#         "status": "reading",
#         "tag_names": ["fantasy", "classic", "adventure"],
#     },
#     {
#         "title": "the book thief",
#         "author": "markus zusak",
#         "pages": 552,
#         "status": "read",
#         "tag_names": ["historical fiction", "war", "young adult"],
#     },
#     {
#         "title": "the martian",
#         "author": "andy weir",
#         "pages": 384,
#         "status": "read",
#         "tag_names": ["sci-fi", "survival", "adventure"],
#     },
# ]

# # add the sample data to the database
# for book_data in books_data:
#  db_actions.add_book(**book_data)
