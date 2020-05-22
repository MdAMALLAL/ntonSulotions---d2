from django.urls import path,reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(),name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("newuser/", views.NewUser.as_view(), name="new"),
    path("profile/<username>",
        views.ProfileView.as_view(),
        name="profile"),
    path("profile/<username>/edit",
        views.ProfileUpdateView.as_view(),
        name="edit"),
    path("profile/<username>/changepassword",
        auth_views.PasswordChangeView.as_view(template_name='accounts/password_change_form.html'),
        name="changepassword"),
    path("password-reset/",
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
                                            email_template_name="accounts/password_reset_email.html",
                                            success_url= reverse_lazy("login")),
        name="password-reset"),


    path("reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',

                                                    success_url= reverse_lazy("home")    ),
        name="password_reset_confirm"),




]
