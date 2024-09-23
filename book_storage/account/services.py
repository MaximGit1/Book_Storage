from .models import Profile


def create_user_profile(user, image) -> Profile:
    return Profile.objects.create(user=user, photo=image)


def get_user_profile(user) -> Profile | None:
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    return profile
