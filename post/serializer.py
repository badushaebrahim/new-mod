from pyexpat import model
from rest_framework import serializers
from .models import posts,comment

class postserializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = posts
        fields = [
            'title',
            'content',
            'created_at',
            'user',
            'comments'
        ]
        depth =2
    def get_comments(self, obj):
        qs = comment.objects.filter(ofpost=obj).count()
        return qs



# class commentserializer(serializers.models):
#     class Meta:
#         model = comment
#         fields = ['comment_text','created_by','created_at']