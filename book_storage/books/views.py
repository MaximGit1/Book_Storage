from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, BookUnit, MarkDownReview
from .forms import CreateMarkDownReviewForm
from . import services


def book_list_view(request: HttpRequest) -> HttpResponse:
    books = services.get_published_books()
    data = {"books": books}
    return render(request, "books/list.html", data)


def book_detail_view(request: HttpRequest, book_slug: str) -> HttpResponse:
    book: Book = get_object_or_404(Book, slug=book_slug, status=Book.Status.PUBLISHED)
    units: QuerySet[BookUnit] = book.units.all()
    data = {"book": book, "units": units}
    return render(request, "books/detail.html", data)


def unit_detail_view(
    request: HttpRequest, book_slug: str, unit_order: int
) -> HttpResponse:
    book: Book = get_object_or_404(Book, slug=book_slug)
    unit: BookUnit = get_object_or_404(BookUnit, book=book, unit_order=unit_order)
    user_review: MarkDownReview | None = MarkDownReview.active.filter(
        unit=unit, author=request.user
    ).first()
    if user_review:
        reviews: QuerySet[MarkDownReview] = MarkDownReview.active.exclude(
            pk=user_review.pk
        ).filter(unit=unit)
    else:
        reviews: QuerySet[MarkDownReview] = MarkDownReview.active.filter(unit=unit)
    data = {"book": book, "unit": unit, "reviews": reviews, "user_review": user_review}
    return render(request, "books/unit/detail.html", data)


def review_detail_view(request: HttpRequest, review_id: int) -> HttpResponse:
    review: MarkDownReview = get_object_or_404(
        MarkDownReview, pk=review_id, is_active=True
    )
    data = {"review": review}
    return render(request, "books/unit/review/detail.html", data)


@login_required
def create_review_view(
    request: HttpRequest, unit_id: int
) -> HttpResponse | HttpResponseRedirect:
    unit: BookUnit = get_object_or_404(BookUnit, pk=unit_id)
    if request.method == "POST":
        form = CreateMarkDownReviewForm(request.POST)
        if form.is_valid():
            review: MarkDownReview = form.save(commit=False)
            review.unit = unit
            review.author = request.user
            review.save()
            return redirect(review.get_absolute_url())
    else:
        form = CreateMarkDownReviewForm()
    data = {"form": form, "unit": unit}
    return render(request, "books/unit/review/create.html", data)
