import requests

req = requests.get("https://www.googleapis.com/books/v1/volumes?q=inauthor:andrzej&key=AIzaSyCFkltepTLq1bnaYuZmK9x9_J4DtZciNzg")
print(req.text)