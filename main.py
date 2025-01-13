from db_actions import dbActions

db_actions = dbActions()


# db_actions.add_book('Harry Potter', 'J.K. Rowling', 500)
# db_actions.remove_book(id= 2)


db_actions.add_book_tag(1, ["sci-fi", "prophecy"])



# if __name__ == "__main__":
#     app = biblotecaApp()
#     app.run()
