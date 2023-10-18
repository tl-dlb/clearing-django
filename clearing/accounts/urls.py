from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("settings/", views.settings, name="settings"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
]
