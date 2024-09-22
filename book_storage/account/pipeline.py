import requests
from .models import Profile
from django.core.files.base import ContentFile


def save_avatar(backend, user, response, *args, **kwargs):
    """
    Save avatar from GitHub to the user profile.
    """
    if backend.name == "github":
        avatar_url = response.get("avatar_url", None)

        if avatar_url:
            profile = Profile.objects.get_or_create(user=user)[0]
            profile_photo = requests.get(avatar_url).content

            filename = f"{user.username}_avatar.jpg"
            profile.photo.save(filename, ContentFile(profile_photo))
            profile.save()
