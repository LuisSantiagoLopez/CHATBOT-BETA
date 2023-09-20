# my_django_app/urls.py

from django.urls import path
from views import decision_tree

urlpatterns = [
 path('/chatapi', decision_tree)
]
