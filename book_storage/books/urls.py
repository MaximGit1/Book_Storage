from django.urls import path
from . import views as v

app_name = "books"

urlpatterns = [
    path("", v.book_list_view, name="book_list"),
    path("book/<slug:book_slug>/", v.book_detail_view, name="book_detail"),
]
