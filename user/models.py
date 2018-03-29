from django.db import models
from django.contrib.auth.models import AbstractUser


class KoinUser(AbstractUser):
    # username = models.CharField(max_length=30)
    # email = models.EmailField()
    secret_key = models.CharField(max_length=32, null=True, blank=True)




