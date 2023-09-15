from rest_framework import serializers 
from .models import ChatSession

class SessionIdSerializer(serializers.ModelSerializer):
 class Meta:
  model = ChatSession
  fields = ['session_id']