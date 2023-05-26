import random
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from library.models import Book


def seed_database():
    # Create 100 books
    for _ in range(100):
        title = get_random_string(length=10)
        author = get_random_string(length=8)
        publication_year = random.randint(1900, 2023)
        category = random.choice(["Fiction", "Non-fiction", "Mystery", "Sci-Fi"])

        book = Book.objects.create(
            title=title,
            author=author,
            publication_year=publication_year,
            category=category,
        )
        book.save()

    print("Seed data created successfully!")
