from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("teacher", views.teacher, name="teacher"),
    path(
        "logout",
        views.logout,
        name="logout",
    ),
    path("webhook", views.github_webhook, name="github_webhook"),
]
