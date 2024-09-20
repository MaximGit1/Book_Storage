from django.utils import timezone
from django.urls import reverse
from django.db import models


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Book.Status.PUBLISHED)


class Author(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Book(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=115)
    slug = models.SlugField(max_length=115)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name="book")
    image = models.ImageField(upload_to="books/books/%Y/%m/")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    class Meta:
        ordering = ["-publish"]

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:book_detail", args=[self.slug])


class BookUnit(models.Model):
    book = models.ForeignKey(to=Book, related_name="units", on_delete=models.CASCADE)
    title = models.CharField(max_length=71)
    description = models.TextField(max_length=155)
    image = models.ImageField(upload_to="books/units/%Y/%m/")
    unit_order = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return f"{(self.book.title)[:6]}: {self.title}:"

    class Meta:
        ordering = ("-book", "unit_order")