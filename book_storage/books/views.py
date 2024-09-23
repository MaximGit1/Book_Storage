from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseNotFound, JsonResponse,
)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import CreateMarkDownReviewForm
from . import services
from django.views.generic import ListView

from .models import BookUnit


class BookListView(ListView):
    template_name = "books/list.html"
    context_object_name = "books"

    def get_queryset(self):
        return services.get_published_books()


def book_detail_view(
    request: HttpRequest, book_slug: str
) -> HttpResponse | HttpResponseNotFound:
    book = services.get_published_book(book_slug)
    if book is None:
        return HttpResponseNotFound("<h1>Not found...</h1>")
    units = services.get_book_units(book)
    data = {"book": book, "units": units}
    return render(request, "books/detail.html", data)


@login_required
def unit_detail_view(
    request: HttpRequest, book_slug: str, unit_order: int
) -> HttpResponse:
    book = services.get_published_book(book_slug)
    if book is None:
        return HttpResponseNotFound("<h1>Not found...</h1>")
    unit = services.get_book_unit(book, unit_order)
    user_review = services.get_user_review(unit, request.user)
    reviews = services.get_active_reviews(unit, exclude_user_review=user_review)
    data = {"book": book, "unit": unit, "reviews": reviews, "user_review": user_review}
    return render(request, "books/unit/detail.html", data)


def review_detail_view(request: HttpRequest, review_id: int) -> HttpResponse:
    review = services.get_active_review(review_id)
    data = {"review": review}
    return render(request, "books/unit/review/detail.html", data)


@login_required
def create_review_view(
    request: HttpRequest, unit_id: int
) -> HttpResponse | HttpResponseRedirect:
    unit = services.get_book_unit_by_id(unit_id)
    if not unit:
        return HttpResponse("Unit not found", status=404)

    if request.method == "POST":
        review = services.create_review_for_unit(unit, request.user, request.POST)
        if review:
            return redirect(review.get_absolute_url())
    else:
        form = CreateMarkDownReviewForm()

    data = {"form": form, "unit": unit}
    return render(request, "books/unit/review/create.html", data)


@login_required
@require_POST
def unit_like_view (request: HttpRequest) -> JsonResponse:
    unit_id = request.POST.get('id')
    action = request.POST.get('action')
    result = services.like_logic(unit_id, action, request.user)
    return JsonResponse(result)


