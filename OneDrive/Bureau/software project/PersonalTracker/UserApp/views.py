from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail

from .forms import RegisterForm, LoginForm, UpdateUserForm
from .models import User, PasswordResetToken


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

    return render(request, "UserApp/signup.html", {"form": form})



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

    return render(request, "UserApp/login.html", {"form": form})



# -------------------------------------------------
# LOGOUT VIEW
# -------------------------------------------------
def logoutView(request):
    logout(request)
    return redirect("login")




@login_required
def profileView(request):
    return render(request, "UserApp/profil.html", {"user": request.user})




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

    return render(request, "UserApp/edit_profile.html", {"form": form})




@login_required
def deleteAccountView(request):
    user = request.user
    user.delete()
    logout(request)
    messages.success(request, "Votre compte a été supprimé avec succès.")
    return redirect("login")



def password_reset_request(request):

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)


            token_obj = PasswordResetToken.generate(user)


            reset_url = request.build_absolute_uri(
                reverse("password_reset_confirm", args=[token_obj.token])
            )

            send_mail(
                subject="Réinitialisation de votre mot de passe",
                message=(
                    f"Bonjour {user.prenom},\n\n"
                    f"Cliquez ici pour réinitialiser votre mot de passe :\n{reset_url}\n\n"
                    "Ce lien expire dans 15 minutes."
                ),
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )

            return redirect("password_reset_sent")

        except User.DoesNotExist:
            messages.error(request, "Cet email n’existe pas dans nos registres.")

    return render(request, "UserApp/password_reset.html")




def password_reset_sent(request):
    return render(request, "UserApp/password_reset_sent.html")




def password_reset_confirm(request, token):


    try:
        token_obj = PasswordResetToken.objects.get(token=token)

        if not token_obj.is_valid():
            return render(request, "UserApp/reset_expired.html")

    except PasswordResetToken.DoesNotExist:
        return render(request, "UserApp/reset_invalid.html")


    if request.method == "POST":
        pwd1 = request.POST.get("password")
        pwd2 = request.POST.get("password2")

        if pwd1 != pwd2:
            messages.error(request, "Les deux mots de passe ne correspondent pas.")
        else:
            user = token_obj.user
            user.set_password(pwd1)
            user.save()

            token_obj.delete()  # token used → delete it

            messages.success(request, "Votre mot de passe a été réinitialisé.")
            return redirect("password_reset_complete")

    return render(request, "UserApp/password_reset_confirm.html")




def password_reset_complete(request):
    return render(request, "UserApp/password_reset_complete.html")
