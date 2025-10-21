from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from main.views import github_webhook

urlpatterns = [
    path("webhook/", github_webhook, name="github_webhook"),
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
