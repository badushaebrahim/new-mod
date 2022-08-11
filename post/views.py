from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import posts
from .serializer import postserializer
# Create your views here.

@api_view(['GET'])
def get_all_post(request):
    if request.method == 'GET':
        postdata = posts.objects.all()
        print(postdata)
        postserial = postserializer(postdata,many=True)
        return Response(postserial.data,status=status.HTTP_200_OK)