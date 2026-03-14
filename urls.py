from django.contrib.auth import views
from django.urls import path, re_path

from .controllers import views
from .controllers import mail
from .controllers import features

urlpatterns = [
    path("", views.index, name="home"),
    re_path(r"^blog/?$", views.blog, name="blog"),
    path("blog/post/<int:post_id>/<str:title>/", views.blog_post, name="blogpost"),
    path("blog/month/<int:year>/<str:month>/", views.blog, name="blog_month"),
    path("blog/tag/<str:tag>/", views.blog, name="blog_tag"),
    re_path(r"^faq/?$", views.faq, name="faq"),
    re_path(r"^pricing/?$", views.pricing, name="pricing"),
    re_path(r"^features/?$", views.features, name="features"),
    re_path(r"^features/static/?$", features.static, name="features_static"),
    re_path(r"^features/second-order/?$", features.second_order, name="features_second_order"),
    re_path(r"^aboutus/?$", views.aboutus, name="aboutus"),
    re_path(r"^contactus/?$", views.contactus, name="contactus"),
    re_path(r"^universities/?$", views.universities, name="universities"),
    re_path(r"^unsubscribe/?$", mail.unsubscribe, name="unsubscribe"),
    re_path(r"^sitemap/?$", views.sitemap, name="sitemap"),
]