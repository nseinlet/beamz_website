from django.contrib.auth import views
from django.urls import path

from .views import aboutus, index, pricing, features

urlpatterns = [
    path("", index, name="home"),
    path("pricing", pricing, name="pricing"),
    path("features", features, name="features"),
    path("aboutus", aboutus, name="aboutus"),
]