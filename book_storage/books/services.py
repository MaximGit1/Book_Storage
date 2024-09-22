from django.db.models import QuerySet
from .models import Book, BookUnit


def get_published_books() -> QuerySet[Book]:
    """returns a querySet of published books"""
    return Book.published.all()


def get_published_book(book_slug: str) -> Book | None:
    """returns the published book if the book slug exists"""
    try:
        book = Book.published.get(slug=book_slug)
    except Book.DoesNotExist:
        book = None
    return book


def get_book_units(book: Book) -> QuerySet[BookUnit]:
    """returns a querySet of book units"""
    return book.units.all()