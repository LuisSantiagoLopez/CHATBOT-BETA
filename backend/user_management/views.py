from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate




