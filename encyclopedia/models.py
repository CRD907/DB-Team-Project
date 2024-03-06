from django.db import models
from django.contrib.auth.models import AbstractUser

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=30)

    
