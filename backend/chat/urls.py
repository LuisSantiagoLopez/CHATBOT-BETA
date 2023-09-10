# my_django_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('auth/signup/', views.user_signup, name='user_signup'),
    path('auth/login/', views.user_login, name='user_login'),
]
