from .models import Book, Author, BookUnit, MarkDownReview
from django.utils.safestring import mark_safe
from django.contrib import admin


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "publish", "status")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("publish", "preview_image")
    search_fields = ("title",)
    list_editable = ("status",)
    fields = ("title", "slug", "author", "preview_image", "image", "status", "publish")

    @staticmethod
    def preview_image(obj: Book):
        return mark_safe(f'<img src="{obj.image.url}" alt="img" width=100px>')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(BookUnit)
class BookUnitAdmin(admin.ModelAdmin):
    list_display = ("book", "title", "unit_order")
    fields = ("title", "preview_image", "image", "description", "unit_order", "book")
    readonly_fields = ("preview_image",)

    @staticmethod
    def preview_image(obj: Book):
        return mark_safe(f'<img src="{obj.image.url}" alt="img" width=150px>')


@admin.register(MarkDownReview)
class MarkDownReviewAdmin(admin.ModelAdmin):
    readonly_fields = ("updated",)
