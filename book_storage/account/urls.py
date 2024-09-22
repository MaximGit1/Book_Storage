from django.urls import path
from . import views as v

app_name = "account"

urlpatterns = [
    path("", v.profile_detail_view, name="self_profile"),
]
