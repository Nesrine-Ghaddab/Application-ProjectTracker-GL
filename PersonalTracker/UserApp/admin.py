from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'nom', 'prenom', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    
    fieldsets = (
        (None, {
            "fields": ("email", "password")
        }),
        ("Informations personnelles", {
            "fields": ("nom", "prenom", "photo", "dateInscription")
        }),
        ("Permissions", {
            "fields": ("role", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nom", "prenom", "password", "role", "is_staff", "is_superuser"),
        }),
    )

    search_fields = ("email", "nom", "prenom")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
