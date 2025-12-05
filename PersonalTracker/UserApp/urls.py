from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", views.registerView, name="register"),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),

    path("profile/", views.profileView, name="profile"),
    path("profile/edit/", views.userUpdateView, name="edit_profile"),
    path("profile/delete/", views.deleteAccountView, name="delete_account"),

    # PASSWORD RESET
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="base_tailwind/password_reset.html"
        ),
        name="password_reset",
    ),

    path(
        "password-reset-sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="base_tailwind/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),

    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="base_tailwind/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),

    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="base_tailwind/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
