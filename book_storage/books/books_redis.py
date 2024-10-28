from redis import Redis
from .models import Book
from os import getenv


class RedisBook:
    def __init__(self, host, port, db):
        super().__init__(host, port, db)
        self.__redis = Redis

    @staticmethod
    def __get_cache_key(book: Book) -> str:
        return f"book:{book.pk}:rating"

    def __get(self, cache_key: str) -> str | None:
        return self.__redis.get(cache_key)

    def __set(self, cache_key: str, units_rating: int, ex: int=3600) -> None:
        self.__redis.set(cache_key, units_rating, ex=3600)

    def get_book_rating(self, book: Book) -> int:
        cache_key = self.__get_cache_key(book)

        rating = self.__get(cache_key)
        if rating:
            return int(rating)

        book_with_units = Book.objects.prefetch_related("units__users_like").get(
            pk=book.pk
        )
        units_rating = sum(
            unit.users_like.count() for unit in book_with_units.units.all()
        )
        self.__set(cache_key, units_rating, ex=3600)

        return units_rating

    def update_book_rating(self, action: str, book: Book) -> int:
        cache_key = self.__get_cache_key(book)
        rating = self.get_book_rating(book)
        match action:
            case "like":
                rating_quantity_delta = 1
            case "unlike":
                rating_quantity_delta = -1
            case _:
                return rating
        new_rating_quantity = rating + rating_quantity_delta
        self.__set(cache_key, new_rating_quantity, ex=3600)
        return new_rating_quantity


redis_book = RedisBook(
    host=getenv("REDIS_HOST"), port=(getenv("REDIS_PORT")), db=getenv("REDIS_DB")
)
