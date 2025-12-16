from django.db import models
from django.contrib.auth.models import AbstractUser

from app.utils.image import compress_image, delete_old_file, delete_file, get_file
from user.managers import UserManager


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    address = models.TextField(blank=True, null=True, help_text="Default shipping address")

    profile_picture = models.ImageField(
        upload_to="profiles/", blank=True, null=True,
        help_text="User profile photo",
    )

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def picture(self) -> str:
        return get_file(None, 'user.jpg')

    def delete(self, *args, **kwargs):
        delete_file(self.profile_picture)
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.profile_picture:
            delete_old_file(self, "profile_picture", self.profile_picture)
            self.profile_picture = compress_image(self.profile_picture)

        super().save(*args, **kwargs)

    def __str__(self):
        full_name = self.get_full_name().strip()
        return full_name if full_name else self.email