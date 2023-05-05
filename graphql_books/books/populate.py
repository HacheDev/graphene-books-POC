import random
from faker import Faker
from .models import Book, Author, Editorial

fake = Faker()


def populate_authors(num):
    for _ in range(num):
        name = fake.name()
        birthdate = fake.date_of_birth()
        death_date = fake.date_of_death() if random.choice([True, False]) else None
        Author.objects.create(name=name, birthdate=birthdate, death_date=death_date)


def populate_editorials(num):
    for _ in range(num):
        name = fake.company()
        Editorial.objects.create(name=name)


def populate_books(num):
    for _ in range(num):
        title = fake.text(max_nb_chars=50)
        summary = fake.text(max_nb_chars=200)
        publish_date = fake.date_between(start_date='-5y', end_date='today')
        author = random.choice(Author.objects.all())
        editorials = list(Editorial.objects.all())
        book = Book.objects.create(title=title, summary=summary, publish_date=publish_date, author=author)
        book.editorial.set(random.sample(editorials, random.randint(1, 3)))
