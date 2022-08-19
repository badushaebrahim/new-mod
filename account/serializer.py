from pyexpat import model
from rest_framework import serializers

from .models import CustomUser

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','first_name','last_name','phone_number','email','password']
        # fields = '__all__'



# class updateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username','first_name','last_name','email','password']