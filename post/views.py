from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from account.models import CustomUser
from .models import posts
from .serializer import postserializer,createpostserializer,postserializer_byid
from account.serializer import loginserializer
# Create your views here.

@api_view(['GET'])
def get_all_post(request):
    if request.method == 'GET':
        postdata = posts.objects.all()
        print(postdata)
        postserial = postserializer(postdata,many=True)
        return Response(postserial.data,status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_new_post(request):
    if request.method == 'POST':
        newpostserial = createpostserializer(data= request.data)
        k= CustomUser.objects.get(pk =request.data["user"])
        ser =  loginserializer(k)
        if str(request.user) == ser.data["first_name"]:
            if newpostserial.is_valid():
                newpostserial.save()
                return Response(newpostserial.data,status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)




class post_rud(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        pass


def get_seriallizer(id,request):
    try:
        postdata = posts.objects.get(pk=id)
        serial  =  postserializer_byid(postdata)
    except posts.DoesNotExist:
        pass