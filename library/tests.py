from django.test import TestCase, RequestFactory
from django.urls import reverse
from library import models
from library.models import Book
from library.views import index
import datetime


# Create your tests here.


class IndexViewTestCase(TestCase):
    def setUp(self):
        # Create some books
        Book.objects.create(
            title="Book 1",
            author="Author 1",
            category="Fiction",
            publication_year=datetime.date(2017, 3, 23),
        )
        Book.objects.create(
            title="Book 2",
            author="Author 2",
            category="Adventure",
            publication_year=datetime.date(2020, 3, 23),
        )

        self.url = reverse("index")

    def test_index_view_with_no_search_query(self):
        response = self.client.get(self.url)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "book_list.html")
        book_titles = [str(book) for book in response.context["books"]]
        # Compare the book titles against the expected values
        expected_titles = ["Book 1", "Book 2"]
        self.assertListEqual(book_titles, expected_titles)

    def test_index_view_with_search_query(self):
        response = self.client.get(self.url, {"search_query": "Author 1"})

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "book_list.html")
        book_titles = [str(book) for book in response.context["books"]]
        # Compare the book titles against the expected values
        expected_titles = ["Book 1"]
        self.assertListEqual(book_titles, expected_titles)

    def test_index_view_error_handling(self):
        response = self.client.get(self.url)

        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Something went wrong:", response.content)
