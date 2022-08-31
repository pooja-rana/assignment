from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

ROLES = (
    ('Admin', 'Admin'),
    ('Solution Provider', 'Solution Provider'),
    ('Solution Seeker', 'Solution Seeker'))


class UserDetail(AbstractUser):
    """Custom user model that supports email instead of username"""

    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    roles = models.CharField(max_length=255, blank=True, null=True, choices=ROLES)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.username)
