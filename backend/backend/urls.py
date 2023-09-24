from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_management/', include('user_management.urls')),
    # path('chatbot/', include('chat.urls')),
    # path('api-token-auth', views.obtain_auth_token),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.jwt')),

]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
"""
Usuario Nuevo Post http://localhost:8000/auth/users/
{
    "email": "ethanordaz@outlook.com",
    "name": "Ethan Ordaz",
    "password": "Nutela173",
    "re_password": "Nutela173"
}
Falta frontend de registro
Activación de Usuario POST http://localhost:8000/auth/users/activation/
{
    "uid": "Mw",
    "token": "bukhdi-04ae57d1fd497006bb481b269f8a9225"
}
uid y token en correo, falta frontend de la verificación
refrescar token de acceso  POST http://localhost:8000/auth/jwt/refresh/
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NDg4ODIwMywiaWF0IjoxNjk0ODAxODAzLCJqdGkiOiI4YjRiZTM4ZDI3ZjM0MmRiYjAwMzE5ZDcyZWIyMDc0YSIsInVzZXJfaWQiOjN9.UyTF-LXxvTghv4tkvky6UnikzEc4Ac42r1RfFakwniY"
}
Obtener token de acceso POST http://localhost:8000/auth/jwt/create/
{
    "email": "ethanordaz@outlook.com",
    "password": "Nutela173"
}
"""
