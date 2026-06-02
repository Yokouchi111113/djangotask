from rest_framework import serializer
from .models import Task 



class TaskSerializer(serializer.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = (
            'id', 
            'user', 
            'created_at', 
            'updated_at',
            )
        

    def create(self, validated_data):

        validated_data['user'] = self.context['request'].user

        return super().create(**validated_data)
        

