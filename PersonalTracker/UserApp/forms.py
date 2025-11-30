from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from captcha.fields import CaptchaField



# Domaines autorisés (modifie selon ton besoin)
ALLOWED_DOMAINS = ["gmail.com", "outlook.com"]


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"})
    )
    captcha = CaptchaField()


    class Meta:
        model = User
        fields = ["nom", "prenom", "email", "password", "photo"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        domain = email.split("@")[-1]

        if domain not in ALLOWED_DOMAINS:
            raise forms.ValidationError(
                "Domaine email non autorisé. Utilisez un email Gmail ou Outlook."
            )

        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Votre email"})
    )
    captcha = CaptchaField()

    def clean_username(self):
        email = self.cleaned_data.get("username")
        domain = email.split("@")[-1]

        if domain not in ALLOWED_DOMAINS:
            raise forms.ValidationError(
                "Domaine email non autorisé. Seuls les emails Gmail ou Outlook sont acceptés."
            )

        return email


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nom", "prenom", "email", "photo"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        domain = email.split("@")[-1]

        if domain not in ALLOWED_DOMAINS:
            raise forms.ValidationError(
                "Vous devez utiliser un email Gmail ou Outlook."
            )

        return email
