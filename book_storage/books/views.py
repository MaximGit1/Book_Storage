from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Book


def book_list_view(request: HttpRequest) -> HttpResponse:
    books: QuerySet[Book] = Book.published.all()
    data = {"books": books}
    return render(request, "books/list.html", data)
