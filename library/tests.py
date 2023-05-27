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

    def test_index_view_with_no_search_query(self):
        url = reverse("index")
        response = self.client.get(url)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "book_list.html")
        book_titles = [str(book) for book in response.context["books"]]
        # Compare the book titles against the expected values
        expected_titles = ["Book 1", "Book 2"]
        self.assertListEqual(book_titles, expected_titles)

    def test_index_view_with_search_query(self):
        url = reverse("index")
        response = self.client.get(url, {"search_query": "Author 1"})

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "book_list.html")
        book_titles = [str(book) for book in response.context["books"]]
        # Compare the book titles against the expected values
        expected_titles = ["Book 1"]
        self.assertListEqual(book_titles, expected_titles)

    def test_index_view_error_handling(self):
        url = reverse("index")
        response = self.client.get(url)

        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Something went wrong:", response.content)


class AddViewTestCase(TestCase):
    def test_add_book_view(self):
        url = reverse("add_book")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_book.html")

        # Test POST request with valid form data
        form_data = {
            "title": "New Book",
            "author": "Author",
            "category": "Fiction",
            "publication_year": "2023-01-01",
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)  # Redirect to index
        self.assertRedirects(response, reverse("index"))

        # Test POST request with invalid form data
        invalid_form_data = {
            "title": "",
            "author": "Author",
            "category": "Fiction",
            "publication_year": "2000-01-01",
        }
        response = self.client.post(url, data=invalid_form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_book.html")
        self.assertFormError(response, "form", "title", "This field is required.")


class DeleteViewTestCase(TestCase):
    def test_delete_book_view(self):
        book = Book.objects.create(
            title="Lord of the rings",
            author="Author 1",
            category="Fantasy",
            publication_year=datetime.date(2001, 3, 23),
        )
        url = reverse("delete_book", args=[book.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # Redirect to index
        self.assertRedirects(response, reverse("index"))

        # Assert that the book is deleted
        self.assertFalse(Book.objects.filter(id=book.id).exists())

        # Test deleting a non-existent book
        non_existent_url = reverse("delete_book", args=[999])
        response = self.client.post(non_existent_url)

        self.assertEqual(response.status_code, 500)
        self.assertIn(b"404: Book not found", response.content)


class EditViewTestCase(TestCase):
    def test_edit_book_view(self):
        book = Book.objects.create(
            title="Book 1",
            author="Author 1",
            category="Fiction",
            publication_year=datetime.date(2020, 3, 23),
        )
        url = reverse("edit_book", args=[book.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_book.html")
        self.assertContains(response, 'value="Book 1"')

        # Test POST request with valid form data
        form_data = {
            "title": "Updated Book",
            "author": "Author",
            "category": "Fiction",
            "publication_year": "2022-01-01",
        }
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)  # Redirect to index
        self.assertRedirects(response, reverse("index"))

        # Assert that the book is updated
        updated_book = Book.objects.get(id=book.id)
        self.assertEqual(updated_book.title, "Updated Book")

        # Test editing a non-existent book
        non_existent_url = reverse("edit_book", args=[999])
        response = self.client.post(non_existent_url)

        self.assertEqual(response.status_code, 500)
        self.assertIn(b"404: Book not found", response.content)
