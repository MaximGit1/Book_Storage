from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase
from .models import Book, Author, BookUnit, MarkDownReview


class TestBook(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            password="test_password",
        )

        self.author = Author.objects.create(
            name="Test author",
        )
        self.book = Book.objects.create(
            title="Test book",
            slug="test-book",
            author=self.author,
            image="image/path.jpeg",
            publish=timezone.now(),
            created=timezone.now(),
            updated=timezone.now(),
            status=Book.Status.PUBLISHED,
        )
        self.unit = BookUnit.objects.create(
            book=self.book,
            title="Unit title",
            description="lorem",
            image="image/path.jpeg",
            unit_order=1,
        )
        self.review = MarkDownReview.objects.create(
            unit=self.unit,
            body="lorem la-la-la",
            author=self.user,
            updated=timezone.now(),
        )

    def test_book_list(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_book_detail(self):
        response = self.client.get("/book/test-book/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.book.title, response.content.decode())

    def test_create_review_redirect(self):
        self.client.login(username="test_user", password="test_password")
        data = {"body": "lorem la-la-la"}
        response = self.client.post(f"/book/review/create/{self.unit.pk}/", data)
        self.assertEqual(response.status_code, 302)

    def test_review_detail(self):
        response = self.client.get(f"/book/review/{self.review.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.review.body, response.content.decode())
