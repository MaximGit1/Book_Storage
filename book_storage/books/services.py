from django.db.models import QuerySet
from .models import Book


def get_published_books() -> QuerySet[Book]:
    """returns a querySet of published books"""
    return Book.published.all()
