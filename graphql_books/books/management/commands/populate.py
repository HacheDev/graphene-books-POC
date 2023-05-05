import os
from datetime import datetime
import json
from django.core.management.base import BaseCommand
import django

from graphql_books.books.models import Author, Editorial, Book


class Command(BaseCommand):
    help = 'Populate database with data from a JSON file whose path is defined in the first argument'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='JSON file containing the data')

    def handle(self, *args, **options):
        filename = options['filename']

        # Read the JSON file
        with open(filename, 'r') as f:
            data = json.load(f)

        for author_data in data['authors']:
            author = Author.objects.create(
                name=author_data['name'],
                birthdate=datetime.strptime(author_data['birthdate'], '%B %d, %Y').date(),
                death_date=datetime.strptime(author_data.get('death_date', ''), '%B %d, %Y').date() if author_data.get(
                    'death_date') else None,
            )

            for book_data in author_data['books']:
                book = Book.objects.create(
                    title=book_data['title'],
                    summary=book_data['summary'],
                    author=author,
                )

                for editorial_data in book_data.get('editorials', []):
                    editorial, _ = Editorial.objects.get_or_create(name=editorial_data['name'])
                    book.editorials.add(editorial)
