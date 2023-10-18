from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRedirect

from .forms import SettingsForm

User = get_user_model()


@require_http_methods(["GET"])
def profile(request: HttpRequest, user_id: int) -> HttpResponse:

    profile = get_object_or_404(User, pk=user_id)


    return TemplateResponse(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            # "articles": articles,
            # "favorites": favorites,
            # "is_following": profile.followers.filter(pk=request.user.id).exists(),
        },
    )


@require_http_methods(["GET", "POST"])
@login_required
def settings(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        return TemplateResponse(
            request,
            "accounts/settings.html",
            {"form": SettingsForm(instance=request.user)},
        )

    if (form := SettingsForm(request.POST, instance=request.user)).is_valid():
        form.save()
        return HttpResponseClientRedirect(request.user.get_absolute_url())

    return TemplateResponse(request, "accounts/_settings.html", {"form": form})





