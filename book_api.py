import requests, json
import configparser
import urllib.parse


# Parse the config file for the api key
config = configparser.ConfigParser()
config.read("config.ini")

api_key = config["google_books"]["api_key"]


# Search request
def search_book(api_key, search_term):
    gb_api_search = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": search_term, "key": api_key}

    r = requests.get(gb_api_search, params=params)
    data = r.json()

    return data


search_term = "Harry Potter"
safe_search_term = urllib.parse.quote(search_term)

books_temp = search_book(api_key, safe_search_term)
print(books_temp)
