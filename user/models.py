from django.db import models
from django.contrib.auth.models import AbstractUser


class KoinUser(AbstractUser):
    secret_key = models.CharField(max_length=32, null=True, blank=True)
    auth_complete = models.BooleanField(default=False)
