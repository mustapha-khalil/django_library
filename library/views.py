from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from .models import Book
from .forms import BookForm

# Create your views here.


def index(request):
    try:
        books = Book.objects.all()
        # books_data = convertQuerySetToList(books)
        return render(request, "book_list.html", {"books": books})

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
