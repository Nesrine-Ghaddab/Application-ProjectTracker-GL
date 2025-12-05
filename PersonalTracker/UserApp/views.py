from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, LoginForm, UpdateUserForm
from .models import User


# -------------------------------------------------
# REGISTER VIEW
# -------------------------------------------------
def registerView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            messages.success(request, "Compte créé avec succès !")
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "base_tailwind/signup.html", {"form": form})


# -------------------------------------------------
# LOGIN VIEW
# -------------------------------------------------
def loginView(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("profile")
            else:
                messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = LoginForm()

    # ❗ IMPORTANT : fichier réel = login.html, pas signin.html
    return render(request, "base_tailwind/login.html", {"form": form})


# -------------------------------------------------
# LOGOUT VIEW
# -------------------------------------------------
def logoutView(request):
    logout(request)
    return redirect("login")


# -------------------------------------------------
# PROFILE VIEW
# -------------------------------------------------
@login_required
def profileView(request):
    return render(request, "base_tailwind/profil.html", {"user": request.user})


# -------------------------------------------------
# UPDATE USER PROFILE
# -------------------------------------------------
@login_required
def userUpdateView(request):
    user = request.user

    if request.method == "POST":
        form = UpdateUserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour !")
            return redirect("profile")

    else:
        form = UpdateUserForm(instance=user)

    return render(request, "base_tailwind/edit_profile.html", {"form": form})


# -------------------------------------------------
# DELETE ACCOUNT
# -------------------------------------------------
@login_required
def deleteAccountView(request):
    user = request.user
    user.delete()
    logout(request)

    messages.success(request, "Votre compte a été supprimé avec succès.")
    return redirect("login")
