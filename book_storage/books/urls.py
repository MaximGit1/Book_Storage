from django.urls import path
from . import views as v

app_name = "books"

urlpatterns = [
    path("", v.book_list_view, name="book_list"),
    path("book/<slug:book_slug>/unit/<int:unit_order>/", v.unit_detail_view, name="unit_detail"),
    path("book/review/create/<int:unit_id>/", v.create_review_view, name="create_review"),
    path("book/review/<int:review_id>/", v.review_detail_view, name="review_detail"),
    path("book/<slug:book_slug>/", v.book_detail_view, name="book_detail"),
]
