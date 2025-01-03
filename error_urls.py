from django.contrib.auth import views
from django.urls import path

from .error_views import error_403, error_404, error_500

urlpatterns = [
    path("403", error_403, name="403"),
    path("404", error_404, name="404"),
    path("500", error_500, name="500"),
]