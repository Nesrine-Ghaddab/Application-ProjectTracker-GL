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


# ===============================
#  VALIDATE IMAGE SIZE (8 MB MAX)
# ===============================
def validate_image_size(image):
    max_size_mb = 8
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"L'image ne doit pas dépasser {max_size_mb} MB.")


# ===============================
#       CUSTOM USER MANAGER
# ===============================
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



# ===============================
#         USER MODEL
# ===============================
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

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nom", "prenom"]

    objects = UserManager()

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.email}"


    # ===============================
    #  IMAGE PROCESSING ON SAVE
    # ===============================
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # No image -> nothing to process
        if not self.photo:
            return

        photo_path = self.photo.path

        # Skip if default image
        if "default.png" in photo_path:
            return

        try:
            img = Image.open(photo_path)

            # Convert to RGB (remove alpha)
            img = img.convert("RGB")

            # -------------------------
            # STEP 1 — RESIZE
            # -------------------------
            max_size = 400
            img.thumbnail((max_size, max_size))


            # -------------------------
            # STEP 2 — CROP TO CIRCLE
            # -------------------------
            np_img = np.array(img)
            h, w = img.size
            diameter = min(h, w)

            alpha_mask = Image.new("L", (diameter, diameter), 0)
            draw = ImageDraw.Draw(alpha_mask)
            draw.ellipse((0, 0, diameter, diameter), fill=255)

            # Center crop square
            img_cropped = img.crop((
                (h - diameter) // 2,
                (w - diameter) // 2,
                (h + diameter) // 2,
                (w + diameter) // 2
            ))

            img_cropped.putalpha(alpha_mask)

            # Convert back to RGB (JPEG doesn't support alpha)
            img_final = img_cropped.convert("RGB")

            # -------------------------
            # STEP 3 — COMPRESS & SAVE
            # -------------------------
            img_final.save(photo_path, "JPEG", quality=85)

        except Exception as e:
            print("Error processing image:", e)
