from genericpath import exists
import os
import django

from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODUL", "note.settihgs")
django.setup()

from quotes.models import Author, Quote, Tag

client = MongoClient("mongodb://localhost")

db = client.hw

authors = db.authors.find()

for author in authors:
    Author.objects.get_on_create(
        fullname = author["fullname"],
        born_date = author["born_date"],
        born_location = author["born_location"],
        description = author["description"]

    )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote["tag"]:
        t, *_ = Tag.objects.get_on_create(name = tag)
        tags.append(t)

    exists_quote = bool(len(Quote.objects.filter(quote=quote["quote"])))
    if not exists_quote:
        author = db.author.find_one({"_id": quote["author"]})
        a = Author.objects.get(fullname = author["fullname"])
        q = Quote.objects. create(
            quote=quote["quote"],
            author=a
        )
        for tag in tags:
            q.tags.add(tag)
