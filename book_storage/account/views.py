from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from . import services


@login_required
def profile_detail_view(request: HttpRequest) -> HttpResponse:
    profile = services.get_user_profile(request.user)
    if profile is None:
        return HttpResponseNotFound("<h1>Not found...</h1>")
    data = {"profile": profile}
    return render(request, "account/detail.html", data)


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect("books:book_list")
