from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils import timezone
from django.core.exceptions import ValidationError
from PIL import Image, ImageDraw
import numpy as np
import os
from datetime import timedelta
from django.utils import timezone
import uuid



def validate_image_size(image):
    max_size_mb = 8
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"L'image ne doit pas dépasser {max_size_mb} MB.")



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
        default="profiles/default.png",
        validators=[validate_image_size]
    )

    dateInscription = models.DateTimeField(default=timezone.now)

    badges = models.ManyToManyField("Badge", blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nom", "prenom"]

    objects = UserManager()

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.email}"



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


        if not self.photo:
            return

        photo_path = self.photo.path


        if "default.png" in photo_path:
            return

        try:
            img = Image.open(photo_path)


            img = img.convert("RGB")


            max_size = 400
            img.thumbnail((max_size, max_size))



            np_img = np.array(img)
            h, w = img.size
            diameter = min(h, w)

            alpha_mask = Image.new("L", (diameter, diameter), 0)
            draw = ImageDraw.Draw(alpha_mask)
            draw.ellipse((0, 0, diameter, diameter), fill=255)


            img_cropped = img.crop((
                (h - diameter) // 2,
                (w - diameter) // 2,
                (h + diameter) // 2,
                (w + diameter) // 2
            ))

            img_cropped.putalpha(alpha_mask)


            img_final = img_cropped.convert("RGB")


            img_final.save(photo_path, "JPEG", quality=85)

        except Exception as e:
            print("Error processing image:", e)

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        """Retourne True si le token est encore valide (15 minutes)."""
        return timezone.now() < self.created_at + timedelta(minutes=15)

    @staticmethod
    def generate(user):
        """Génère un token unique pour un utilisateur."""
        token = uuid.uuid4().hex
        return PasswordResetToken.objects.create(user=user, token=token)

    def __str__(self):
        return f"Token for {self.user.email} created at {self.created_at}"
    

class Badge(models.Model):
    name = models.CharField(max_length=50)
    emoji = models.CharField(max_length=5, help_text="Ex: 🔥, ⭐, 🏅")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.emoji} {self.name}"
    
   


