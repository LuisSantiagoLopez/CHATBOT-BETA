from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_description = models.TextField(null=True, blank=True)
    target_audience = models.TextField(null=True, blank=True)
    writing_style = models.TextField(null=True, blank=True)
    image_style = models.TextField(null=True, blank=True)

class Subscription(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)