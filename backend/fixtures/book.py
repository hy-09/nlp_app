import os
import requests
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from django import setup

setup()

from api.models import Book

url = 'https://api.bungomail.com/v0/books'
res = requests.get(url)

books = json.loads(res.text)['books']

for book in books:
    new_book = Book(
        title=book['作品名'],
        url=book['テキストファイルURL']
    )
    new_book.save()