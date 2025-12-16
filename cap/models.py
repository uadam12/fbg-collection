from decimal import Decimal
from django.db import models
from app.utils.image import get_file, delete_old_file, delete_file, compress_image


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Cap(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='caps/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="caps")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    description = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)


    class Meta:
        ordering = ["name"]

    @property
    def picture(self):
        return get_file(self.image, 'cap.jpg')

    def delete(self, *args, **kwargs):
        delete_file(self.image)
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.image:
            delete_old_file(self, "image", self.image)
            self.image = compress_image(self.image)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name