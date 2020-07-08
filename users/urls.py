from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


app_name = "users"

urlpatterns = [
    # path("register", views.register, name="register"),
    path("register/", views.SignUpPageView.as_view(), name="register"),
    path("update_profile/", views.private_profile, name="update_profile"),
    path("public_profile/<uuid:user_id>/",
         views.PublicProfile, name="public_profile")
]
