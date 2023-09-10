from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_management/',include('user_management.urls')),
    path('chatbot/',include('chat.urls')),
    path('api-token-auth', views.obtain_auth_token)
]
