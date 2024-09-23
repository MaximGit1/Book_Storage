from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Model
from django.http import JsonResponse

from .models import Book, BookUnit, MarkDownReview
from .forms import CreateMarkDownReviewForm


User = get_user_model()


def get_published_books() -> QuerySet[Book]:
    """returns a querySet of published books"""
    return Book.published.all()


def _try_to_get_object(model: Model, **kwargs) -> Model | None:
    try:
        obj = model.objects.get(**kwargs)
    except (model.DoesNotExist, model.MultipleObjectsReturned):
        obj = None
    return obj


def get_published_book(book_slug: str) -> Book | None:
    """returns the published book if the book slug exists"""
    return _try_to_get_object(Book, slug=book_slug, status=Book.Status.PUBLISHED)


def get_book_units(book: Book) -> QuerySet[BookUnit]:
    """returns a querySet of book units"""
    return book.units.all()


### through **kwargs, need to update views
def get_book_unit(book: Book, unit_order: int) -> BookUnit | None:
    """returns the specific book unit"""
    return _try_to_get_object(BookUnit, book=book, unit_order=unit_order)


def get_book_unit_by_id(unit_id: int):
    return _try_to_get_object(BookUnit, pk=unit_id)


###


def get_user_review(unit: BookUnit, author: User) -> MarkDownReview | None:
    """returns the user's review (MarkDownReview) for the specified unit"""
    return _try_to_get_object(MarkDownReview, unit=unit, author=author, is_active=True)


def get_active_reviews(
    unit: BookUnit, exclude_user_review: MarkDownReview | None = None
) -> QuerySet[MarkDownReview]:
    """returns active units reviews, you can get querySet without the review of the passed user"""
    if exclude_user_review:
        reviews = MarkDownReview.active.exclude(pk=exclude_user_review.pk).filter(
            unit=unit
        )
    else:
        reviews = MarkDownReview.active.filter(unit=unit)
    return reviews


def get_active_review(review_id: int):
    return _try_to_get_object(MarkDownReview, pk=review_id, is_active=True)


def create_review_for_unit(
    unit: BookUnit, author: User, post_data
) -> MarkDownReview | None:
    form = CreateMarkDownReviewForm(post_data)
    if form.is_valid():
        review = form.save(commit=False)
        review.unit = unit
        review.author = author
        review.save()
        return review
    return None


def like_logic(unit_id: int, action: str, user: User) -> dict[str, str]:
    if unit_id and action:
        try:
            unit = get_book_unit_by_id(unit_id)
            if not unit:
                return {'status': 'error'}  # Возвращаем ошибку, если юнит не найден

            if action == "like":
                unit.users_like.add(user)
            elif action == "unlike":
                unit.users_like.remove(user)
            else:
                return {'status': 'error'}
            return {'status': 'ok'}
        except BookUnit.DoesNotExist:
            return {'status': 'error'}
    return {'status': 'error'}