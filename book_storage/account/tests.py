from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from . import services

User = get_user_model()


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testUser", password="password12")
        self.profile = services.create_user_profile(self.user, "image.png")

    def test_profile_detail_view(self):
        self.client.login(username="testUser", password="password12")
        response = self.client.get(reverse("account:self_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/detail.html")
        self.assertEqual(response.context["profile"], self.profile)

    def test_logout_view(self):
        self.client.login(username="testUser", password="password12")
        response = self.client.get(reverse("account:self_profile"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        response = self.client.get(reverse("account:logout"))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("account:self_profile"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
