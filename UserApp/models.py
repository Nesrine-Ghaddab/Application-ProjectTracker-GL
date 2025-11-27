from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils import timezone


class UserManager(BaseUserManager):
    
    def create_user(self, email, nom, prenom, password=None, role="user"):
        if not email:
            raise ValueError("L'email est obligatoire")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            nom=nom,
            prenom=prenom,
            role=role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, nom, prenom, password=None):
        user = self.create_user(
            email=email,
            nom=nom,
            prenom=prenom,
            password=password,
            role="admin"
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    
    id_user = models.AutoField(primary_key=True)
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    
    email = models.EmailField(unique=True)
    
    role = models.CharField(
        max_length=20,
        choices=[("admin", "Admin"), ("user", "User")],
        default="user"
    )
    
    photo = models.ImageField(
        upload_to="profiles/",
        default="profiles/default.png"
    )
    
    dateInscription = models.DateTimeField(default=timezone.now)

    # Nécessaires pour Django Admin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nom", "prenom"]

    objects = UserManager()

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.email}"