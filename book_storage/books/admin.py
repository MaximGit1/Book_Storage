from django.contrib import admin
from .models import Book, Author, BookUnit, MarkDownReview
from django.utils.safestring import mark_safe


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "publish", "status")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("publish", "preview_image")
    search_fields = ("title",)
    list_editable = ("status",)
    fields = ("title", "slug", "author", "preview_image", "image", "status", "publish")

    def preview_image(self, obj: Book):
        return mark_safe(f'<img src="{obj.image.url}" alt="img" width=100px>')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(BookUnit)
class BookUnitAdmin(admin.ModelAdmin):
    list_display = ("book", "title", "unit_order")
    fields = ("title", "preview_image", "image", "description", "unit_order", "book")
    readonly_fields = ("book", "preview_image")

    def preview_image(self, obj: Book):
        return mark_safe(f'<img src="{obj.image.url}" alt="img" width=150px>')


@admin.register(MarkDownReview)
class MarkDownReviewAdmin(admin.ModelAdmin):
    readonly_fields = ("updated",)
