from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4

# Modelo para guardar el usuario
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# Esto no está conectado a nada, se supone que servirá para conectar stripe 
class Subscription(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    active = models.BooleanField(default=True)