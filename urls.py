from django.contrib.auth import views
from django.urls import path

from .views import index

urlpatterns = [
    path("", index, name="register"),
]