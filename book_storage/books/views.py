from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Book, BookUnit


def book_list_view(request: HttpRequest) -> HttpResponse:
    books: QuerySet[Book] = Book.published.all()
    data = {"books": books}
    return render(request, "books/list.html", data)

def book_detail_view(request: HttpRequest, book_slug: str) -> HttpResponse:
    book: Book = get_object_or_404(Book, slug=book_slug, status=Book.Status.PUBLISHED)
    units: QuerySet[BookUnit] = book.units.all()
    data = {'book': book, 'units': units}
    return render(request, "books/detail.html", data)
