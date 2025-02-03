import requests, json
import configparser
import urllib.parse


# Parse the config file for the api key
config = configparser.ConfigParser()
config.read("config.ini")

api_key = config["google_books"]["api_key"]


# Search request
def search_book(api_key, search_term, max_results):
    gb_api_search = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": search_term, "key": api_key, "maxResults": max_results}

    r = requests.get(gb_api_search, params=params)
    data = r.json()

    return data


search_term = "Harry Potter Philosopher's Stone"
safe_search_term = urllib.parse.quote(search_term)

books_temp = search_book(api_key, safe_search_term, 3)
formatted_json = json.dumps(books_temp, indent=4)
print(formatted_json)
