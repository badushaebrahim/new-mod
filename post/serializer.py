from asyncore import read
from pyexpat import model
from rest_framework import serializers
from .models import posts,comment

class commentserializer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = '__all__'


class commentgetserialiser (serializers.ModelSerializer):
    # post = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = comment
        fields = ['id','comment_text','ofpost','created_by']
        
        # def get_post(self,obj)
        



class postserializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = posts
        fields = [
            'title',
            'content',
            'created_at',
            'comments'
        ]
        # depth =1
    def get_comments(self, obj):
        qs = comment.objects.all().filter(ofpost=obj)
        print(type(qs))
        qs2 = commentserializer(qs,many=True)
        print(qs2.data)
        return qs2.data



class createpostserializer(serializers.ModelSerializer):
    class Meta:
        model =  posts
        fields = [
            'title',
            'content',
            'user'
        ]

class postserializer_byid(serializers.ModelSerializer):
    # comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = posts
        fields = [
            'title',
            'content',
            'user'
        ]
