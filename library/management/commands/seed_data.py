import random
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from library.models import Book


class Command(BaseCommand):
    help = "Seeds the database with sample data"

    def handle(self, *args, **options):
        # Create 10 books
        for _ in range(10):
            title = get_random_string(length=10)
            author = get_random_string(length=8)
            year = random.randint(1900, 2023)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            publication_year = f"{year:04d}-{month:02d}-{day:02d}"
            category = random.choice(["Fiction", "Non-fiction", "Mystery", "Sci-Fi"])

            book = Book.objects.create(
                title=title,
                author=author,
                publication_year=publication_year,
                category=category,
            )
            book.save()

        self.stdout.write(self.style.SUCCESS("Seed data created successfully!"))
