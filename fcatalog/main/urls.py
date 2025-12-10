from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("teacher/", views.teacher, name="teacher"),
    path("logout/", views.logout, name="logout"),
    path("discipline_requests/", views.discipline_requests, name="discipline_requests"),
    path("test/", views.test_exec, name="testing"),
    path("webhook/", views.github_webhook, name="github_webhook"),
    
    # path("", views.general, name="general"),
    # path("login/", views.login, name="login"),
    # path("teacher/", views.teacher, name="teacher"),
    # path("webhook/", views.github_webhook, name="github_webhook"),
]
