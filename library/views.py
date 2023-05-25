from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse, HttpResponseServerError
from .models import Book
from .forms import BookForm

# Create your views here.


def index(request):
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
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = BookForm()

    return render(request, "add_book.html", {"form": form})


def deleteBook(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return redirect("index")
    except Book.DoesNotExist:
        return HttpResponseServerError("404: Book not found")
    except Exception as e:
        return HttpResponseServerError("Something went wrong: " + str(e))


def editBook(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponseServerError("Book does not exist.")

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = BookForm(instance=book)

    return render(request, "edit_book.html", {"form": form, "book_id": book.id})
