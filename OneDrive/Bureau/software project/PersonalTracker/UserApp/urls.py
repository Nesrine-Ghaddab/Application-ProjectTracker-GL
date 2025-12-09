from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("register/", views.registerView, name="register"),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),

    # Profile
    path("profile/", views.profileView, name="profile"),
    path("profile/edit/", views.userUpdateView, name="edit_profile"),
    path("profile/delete/", views.deleteAccountView, name="delete_account"),

    # Password Reset (Custom)
    path("password-reset/", views.password_reset_request, name="password_reset"),
    path("password-reset-sent/", views.password_reset_sent, name="password_reset_sent"),
    path("password-reset-confirm/<str:token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("password-reset-complete/", views.password_reset_complete, name="password_reset_complete"),
]
