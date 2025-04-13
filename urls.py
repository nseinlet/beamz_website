from django.contrib.auth import views
from django.urls import path

from .views import aboutus, blog, index, pricing, features, faq, blog_post

urlpatterns = [
    path("", index, name="home"),
    path("blog", blog, name="blog"),
    path("blog/post/<int:post_id>/<str:title>/", blog_post, name="blogpost"),
    path("blog/month/<int:year>/<str:month>/", blog, name="blog_month"),
    path("blog/tag/<str:tag>/", blog, name="blog_tag"),
    path("faq", faq, name="faq"),
    path("pricing", pricing, name="pricing"),
    path("features", features, name="features"),
    path("aboutus", aboutus, name="aboutus"),
]