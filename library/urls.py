from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.addBook, name="add_book"),
    path("<int:book_id>/", views.editBook),
    path("<int:book_id>/delete", views.deleteBook),
]
