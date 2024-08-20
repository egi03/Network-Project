
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<str:username>", views.show_profile, name="show_profile"),
    path("toggle_follow", views.toggle_follow, name="toggle_follow"),
    path("following", views.following_view, name="following"),
    
    # API Routes
    path("edit_post", views.edit_post, name="edit_post")
]
