from django.urls import path,reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(),name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('ajax/load_notification/',views.get_new_notification, name='load_notification'),
    path('notifications/',views.NotificationView.as_view(), name='notifications'),
    path('notifications/<pk>',views.notifications_redirectView, name='notifications_redirect'),
    path('notifications/<pk>/remove/',views.notifications_remove, name='notifications_remove'),
    path('notifications/<pk>/mark_as_read',views.notifications_markread, name='notifications_markread'),

    path("profile/",
        views.myProfileView,
        name="myprofile"),
    path("change_password",
        views.UserPasswordChang.as_view(),
        name="changepassword"),
    path("profile/<username>/edit",
        views.ProfileUpdateView.as_view(),
        name="edit"),
    path("ajax/made_consultant/<username>", views.made_consultant, name="made-consultant"),

    path("", views.UserListView.as_view(), name="list"),

    path("profile/<username>",
        views.ProfileUpdateView.as_view(),
        name="profile"),


    path("password-reset/",
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
                                            email_template_name="accounts/password_reset_email.html",
                                            success_url= reverse_lazy("login")),
        name="password-reset"),
    path("reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',

                                                    success_url= reverse_lazy("home")    ),
        name="password_reset_confirm"),
    path("new_user/", views.NewUser.as_view(), name="new"),


]
