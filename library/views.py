from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from .models import Book
from .forms import BookForm

# Create your views here.


def index(request):
    try:
        books = Book.objects.all()
        # Convert books queryset to a list of dictionaries
        books_data = [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "publication_year": book.publication_year,
                "category": book.category,
            }
            for book in books
        ]
        return JsonResponse({"books": books_data})

    except Exception as e:
        error_message = "Something went wrong: " + str(e)
        return HttpResponseServerError(error_message)


def addBook(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = BookForm()

    return render(request, "add_book.html", {"form": form})


def editBook(request, book_id):
    return HttpResponse("Your are editing the book %s." % book_id)


def deleteBook(request, book_id):
    return HttpResponse("You are deleting book %d" % book_id)
