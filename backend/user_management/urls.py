from django.urls import path
from .views import RegisterUserAPIView, UserProfileView, VerifyEmailAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('signup/', RegisterUserAPIView.as_view(), name='signup'),
    path('verify-email/<uuid:token>/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('signin/', LoginAPIView.as_view(), name='signin'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
