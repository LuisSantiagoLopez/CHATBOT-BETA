from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4

# Modelo para guardar el usuario
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Estas son cosas que le vamos a preguntar al usuario cuando hagamos el chatbot para generarle contenido relevante
    business_description = models.TextField(null=True, blank=True)
    target_audience = models.TextField(null=True, blank=True)
    writing_style = models.TextField(null=True, blank=True)
    image_style = models.TextField(null=True, blank=True)

# Esto no está conectado a nada, se supone que servirá para conectar stripe 
class Subscription(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

# Esto no sirve... se supone que es para crear el token para autenticar el email del usuario 
class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)