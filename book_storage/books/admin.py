from django.contrib import admin
from .models import Book, Author


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "publish", "status")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish"
    exclude = ["publish"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
