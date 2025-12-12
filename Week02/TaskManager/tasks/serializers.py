from rest_framework import serializers
from .models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'categ_name']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'priority', 
                  'status', 'due_date', 'category', 'created_at')
        # prevents the user from trying to change the 'id' or 'created_at' date.
        read_only_fields = ['id', 'created_at']