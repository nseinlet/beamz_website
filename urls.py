from django.contrib.auth import views
from django.urls import path

from .views import aboutus, index, pricing

urlpatterns = [
    path("", index, name="home"),
    path("pricing", pricing, name="pricing"),
    path("aboutus", aboutus, name="aboutus"),
]