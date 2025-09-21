from django.db import models
from django.conf import settings

# Create your models here.
class LoginModel(models.Model):
    nome = models.CharField(max_length=100)


class Product(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = (('owner', 'name'),)

    def __str__(self) -> str:
        return f"{self.name} ({self.quantity})"
