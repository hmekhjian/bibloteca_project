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
    params = {
        "q": search_term,
        "key": api_key,
        "maxResults": max_results,
        "printType": "books",
        "orderBy": "relevance",
    }

    r = requests.get(gb_api_search, params=params)
    data = r.json()

    return data



def safe_search_term(search_term):
    return urllib.parse.quote(search_term)
    

# books_temp = search_book(api_key, safe_search_term, 5)
# formatted_json = json.dumps(books_temp, indent=4)

# for item in books_temp["items"]:
#     print(item["volumeInfo"]["title"])
