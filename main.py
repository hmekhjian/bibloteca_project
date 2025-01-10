from db_actions import dbActions

db_actions = dbActions()


# db_actions.add_book('Harry Potter', 'J.K. Rowling', 500)
# db_actions.remove_book(id= 2)

# class biblotecaApp(App):

print(db_actions.list_books())

# if __name__ == "__main__":
#     app = biblotecaApp()
#     app.run()