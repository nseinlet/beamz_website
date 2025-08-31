from django.contrib.auth import views
from django.urls import path

from .controllers import views
from .controllers import mail

urlpatterns = [
    path("", views.index, name="home"),
    path("blog", views.blog, name="blog"),
    path("blog/post/<int:post_id>/<str:title>/", views.blog_post, name="blogpost"),
    path("blog/month/<int:year>/<str:month>/", views.blog, name="blog_month"),
    path("blog/tag/<str:tag>/", views.blog, name="blog_tag"),
    path("faq", views.faq, name="faq"),
    path("pricing", views.pricing, name="pricing"),
    path("features", views.features, name="features"),
    path("aboutus", views.aboutus, name="aboutus"),
    path("contactus", views.contactus, name="contactus"),
    path("universities", views.universities, name="universities"),
    path("unsubscribe", mail.unsubscribe, name="unsubscribe"),
]