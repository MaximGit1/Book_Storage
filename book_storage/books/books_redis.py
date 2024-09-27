from redis import Redis
from .models import Book
from os import getenv


class RedisBook(Redis):
    def __init__(self, host, port, db):
        super().__init__(host, port, db)

    @staticmethod
    def get_cache_key(book: Book) -> str:
        return f"book:{book.pk}:rating"

    def get_book_rating(self, book: Book) -> int:
        cache_key = self.get_cache_key(book)

        rating = self.get(cache_key)
        if rating:
            return int(rating)

        book_with_units = Book.objects.prefetch_related("units__users_like").get(
            pk=book.pk
        )
        units_rating = sum(
            unit.users_like.count() for unit in book_with_units.units.all()
        )
        self.set(cache_key, units_rating, ex=3600)

        return units_rating

    def update_book_rating(self, action: str, book: Book) -> int:
        cache_key = self.get_cache_key(book)
        rating = self.get_book_rating(book)
        match action:
            case "like":
                rating_quantity_delta = 1
            case "unlike":
                rating_quantity_delta = -1
            case _:
                return rating
        new_rating_quantity = rating + rating_quantity_delta
        self.set(cache_key, new_rating_quantity, ex=3600)
        return new_rating_quantity


redis_book = RedisBook(
    host=getenv("REDIS_HOST"), port=(getenv("REDIS_PORT")), db=getenv("REDIS_DB")
)
