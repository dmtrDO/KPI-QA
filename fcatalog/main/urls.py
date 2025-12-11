from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("teacher/disciplines", views.teacher_discips, name="teacher_discips"),
    path("teacher/description", views.teacher_descrip, name="teacher_descrip"),
    path("discipline_requests/", views.discipline_requests, name="discipline_requests"),
    path("webhook/", views.github_webhook, name="github_webhook"),
    
    # path("disciplines/", views.general_discips, name="general_discips"),
    # path("description/", views.general_descrip, name="general_descrip"),
    
    # path("test/", views.test_exec, name="testing"),
    # path("teacher/", views.teacher_gen, name="teacher"),
    # path("", views.general, name="general"),
    # path("login/", views.login, name="login"),
    # path("teacher/", views.teacher, name="teacher"),
    # path("webhook/", views.github_webhook, name="github_webhook"),
]
