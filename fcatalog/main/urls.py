from django.urls import path
from . import views

urlpatterns = [
    path("", views.general, name="general"),
    path("login/", views.login, name="login"),
    path("teacher/", views.teacher, name="teacher"),
    path("webhook/", views.github_webhook, name="github_webhook"),
]
