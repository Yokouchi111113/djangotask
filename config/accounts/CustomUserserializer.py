from rest_framework import serializer
from .models import CustomUser

class CustomUserSerializer(serializer.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'display_name']
        read_only_fields = ['email']