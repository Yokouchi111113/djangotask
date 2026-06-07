from rest_framework import serializers
from .models import Task 
from django.utils import timezone



class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = (
            'id', 
            'user', 
            'created_at', 
            'updated_at',
            )
        

    def validate_due_date(self, value):

        if value and value < timezone.now().date():
            raise serializers.ValidationError(
                "過去の日付は設定できません"
            )

        return value
