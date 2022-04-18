from sre_constants import JUMP
import requests, json

searchTerm = 'Dune'
response = requests.get("http://openlibrary.org/search.json?q=Dune&limit=1")

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


data = response.json()
print(data['docs'][0]['first_publish_year'])
print(data['docs'][0]['number_of_pages_median'])
print(data['docs'][0]['author_name'][0])
