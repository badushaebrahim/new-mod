from rest_framework import serializers
from .models import posts,comment

class CommentGetSerialiser (serializers.ModelSerializer):
    '''comment serializer for comment crud'''
    class Meta:
        '''comment serializer'''
        model = comment
        fields = ['id','comment_text','ofpost','created_by']

class PostSerializer(serializers.ModelSerializer):
    '''post serializer'''
    comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        '''meta of post with fields and models'''
        model = posts
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'comments'
        ]
        # depth =1
    def get_comments(self, obj):
        '''this function is used to retrive allthe comment of the post'''
        qs = comment.objects.all().filter(ofpost=obj)
        qs2 = CommentGetSerialiser(qs,many=True)
        return qs2.data

class CreatePostSerializer(serializers.ModelSerializer):
    '''create post serializer'''
    class Meta:
        '''model and field for seralizer'''
        model =  posts
        fields = [
            'title',
            'content',
            'user'
        ]
