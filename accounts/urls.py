from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(),name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("newuser/", views.NewUser.as_view(), name="new"),
    path("profile/<username>", views.ProfileView.as_view(), name="profile"),
    path("profile/<username>/update", views.ProfileUpdateView.as_view(), name="profileUpdate"),


]
