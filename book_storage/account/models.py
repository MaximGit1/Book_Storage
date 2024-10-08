from django.conf import settings
from django.db import models
from pathlib import Path


# these functions are here because otherwise cyclic import occurs
def create_user_filename(instance, filename: str) -> str:
    """
    Generates a filename to save the image using the username.
    Example path: 'username.ext'
    """
    ext = filename.split(".")[-1]
    filename = f"{instance.user.username}.{ext}"
    return str(Path(filename))


def create_user_directory_path(instance, filename: str) -> str:
    """
    Generates a path to save the image using the username.
    Example path: 'users/username.ext'
    """
    filename = create_user_filename(instance, filename)
    return str(Path(f"users/").joinpath(filename))


class Profile(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    photo = models.ImageField(upload_to=create_user_directory_path, blank=True)
    about = models.TextField(blank=True, max_length=150)

    def __str__(self):
        return f"Profile of {self.user.username}"
