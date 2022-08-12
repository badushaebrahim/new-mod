from pstats import Stats
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


'''
to get all post and comments
'''
@api_view(['GET'])
def get_all_post(request):
    if request.method == 'GET':
        postdata = posts.objects.all()
        print(postdata)
        postserial = postserializer(postdata,many=True)
        return Response(postserial.data,status=status.HTTP_200_OK)

'''
mycontent with userid
'''

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_content(request,id):
    if request.method == 'GET':
        try:
            postdata = posts.objects.all().filter(user=id)
            postserial = postserializer(postdata,many=True)
            return Response(postserial.data,status=status.HTTP_200_OK)
        except posts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


'''
to create post if you are a logedin user
'''

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
                return Response(newpostserial.data,status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


'''
class to read , update ,delete post based  on post id 
'''

class post_rud(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id,*args,**kwargs):
        errrors = False
        serial ,errors = get_seriallizer_of_post(id,request)
        if errors == True:
            return serial
        return Response(serial.data)
    
    def put(self,request,id,*args,**kwargs):
        errors = False
        serial , errors = get_model_of_post(id,request)
        if errors == True:
            return serial
        else :
            ser = postserializer(serial,data=request)
            if ser.is_valid():
                ser.save()
                return Response(ser.data,status=status.HTTP_200_OK)
            return Response(status= status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,*args,**kwargs):
        errors =False
        serial,errors = get_model_of_post(id,request)
        if errors == True:
            serial.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        pass




'''
function that check if user is owner of the post and return serializer for read
'''
def get_seriallizer_of_post(id,request):
    try:
        postdata = posts.objects.get(pk=id)
        serial  =  postserializer_byid(postdata)
        userdata= CustomUser.objects.get(pk = serial.data["user"])
        userserial = loginserializer(userdata)
        if str(request.user) == userserial.data["first_name"]:
            return serial,False
        print("else")
        return Response(status=status.HTTP_403_FORBIDDEN),True

    except posts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND),True

'''
function to check if user is owner of the 
post and return model for put,delete 
'''

def get_model_of_post(id,request):
    try:
        postdata = posts.objects.get(pk=id)
        serial  =  postserializer_byid(postdata)
        userdata= CustomUser.objects.get(pk = serial.data["user"])
        userserial = loginserializer(userdata)
        if str(request.user) == userserial.data["first_name"]:
            return postdata,False
        print("else")
        return Response(status=status.HTTP_403_FORBIDDEN),True

    except posts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND),True