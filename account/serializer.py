from rest_framework import serializers

from .models import CustomUser

class LoginSerializer(serializers.ModelSerializer):
    '''serializer for user'''
    class Meta:
        '''mdoel serializer for user'''
        model = CustomUser
        fields = ['id','username','first_name','last_name','phone_number','email','password']
