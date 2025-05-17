from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    phone   = models.CharField("Phone Number", max_length=20, blank=True)
    address = models.CharField("Address", max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"