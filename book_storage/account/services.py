from pathlib import Path

from .models import Profile


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


def create_user_profile(user, image) -> Profile:
    return Profile.objects.create(user=user, photo=image)


def get_user_profile(user) -> Profile | None:
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    return profile
