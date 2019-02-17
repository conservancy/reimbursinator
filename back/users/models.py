from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model to allow for new fields if necessary.
    """
    age = models.PositiveIntegerField(null=True, blank=True)
