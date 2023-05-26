from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponseServerError
from .models import Book
from .forms import BookForm

# Create your views here.


def index(request):
    """
    View function for displaying the book index page.
    Retrieves books from the database based on the search query, if provided.
    Otherwise, retrieves all books.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered book index page.

    Raises:
        HttpResponseServerError: If an error occurs while retrieving books from the database.
    """

    try:
        search_query = request.GET.get("search_query", "")

        if search_query:
            books = Book.objects.filter(
                Q(title__icontains=search_query)
                | Q(author__icontains=search_query)
                | Q(category__icontains=search_query)
            )
        else:
            books = Book.objects.all()

        return render(request, "book_list.html", {"books": books})

    except Exception as e:
        return HttpResponseServerError("Something went wrong: " + str(e))


def addBook(request):
    """
    View function for adding a new book.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered add book form or a redirect response.

    Raises:
        HttpResponseServerError: If an error occurs while retrieving books from the database.
    """

    try:
        if request.method == "POST":
            form = BookForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("index")
        else:
            form = BookForm()

        return render(request, "add_book.html", {"form": form})

    except Exception as e:
        return HttpResponseServerError("Something went wrong: " + str(e))


def deleteBook(request, book_id):
    """
    View function for deleting a book.

    Args:
        request (HttpRequest): The HTTP request object.
        book_id (int): The ID of the book to be deleted.

    Returns:
        HttpResponse: The HTTP redirect response to the book index page if the book is deleted successfully.

    Raises:
        HttpResponseServerError: If an error occurs while retrieving books from the database or if book is not found.
    """

    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return redirect("index")
    except Book.DoesNotExist:
        return HttpResponseServerError("404: Book not found")
    except Exception as e:
        return HttpResponseServerError("Something went wrong: " + str(e))


def editBook(request, book_id):
    """
    View function for editing a book.

    Args:
        request (HttpRequest): The HTTP request object.
        book_id (int): The ID of the book to be edited.

    Returns:
        HttpResponse: The HTTP response to render the edit book form or the HTTP redirect response to the book index page if the book is edited successfully.

    Raises:
        HttpResponseServerError: If an error occurs while retrieving books from the database or if the book is not found.
    """

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponseServerError("404: Book not found.")

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = BookForm(instance=book)

    return render(request, "edit_book.html", {"form": form, "book_id": book.id})
