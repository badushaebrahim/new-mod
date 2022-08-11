from rest_framework import serializers
from .models import posts

class postserializer(serializers.ModelSerializer):
    class Meta:
        model = posts
        fields = [
            'title',
            'content',
            'created_at',
            'user',
            'comment'
        ]
        depth =1