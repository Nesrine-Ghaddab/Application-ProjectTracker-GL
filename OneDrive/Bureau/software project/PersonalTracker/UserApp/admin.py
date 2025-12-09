from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Badge


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
        ("Badges", {                            # <--- AJOUT ICI
            "fields": ("badges",)               # <--- AJOUT ICI
        }),
        ("Permissions", {
            "fields": ("role", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "nom", "prenom", "password",
                "role", "is_staff", "is_superuser",
                "badges",                           # <--- AJOUT ICI
            ),
        }),
    )

    search_fields = ("email", "nom", "prenom")
    ordering = ("email",)

    filter_horizontal = ("badges",)               # <--- AJOUT IMPORTANT


admin.site.register(User, CustomUserAdmin)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "emoji", "description")
