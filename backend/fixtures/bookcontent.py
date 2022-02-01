import os
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from django import setup

setup()

from api.models import Book
from api.util.chart import get_content_chart

books = Book.objects.all()

for book in books:
    content, chart = get_content_chart(book.id, book.url)