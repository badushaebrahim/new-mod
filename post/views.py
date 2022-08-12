from asyncio import new_event_loop
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
from .serializer import commentserializer, postserializer,createpostserializer,postserializer_byid
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
mycontent with userid and only content i created
'''

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_content(request):
    if request.method == 'GET':
        print(request.user)
        try:
            userdata = CustomUser.objects.get(first_name = request.user)
            userserial = loginserializer(userdata)
            # print("user id",userserial.data['id'])
            try:
                postdata = posts.objects.all().filter(user=int(userserial.data['id']))
                if str(request.user) == str(userserial.data["first_name"]):
                    postserial = postserializer(postdata,many=True)
                    return Response(postserial.data,status=status.HTTP_200_OK)
                return Response(status=status.HTTP_403_FORBIDDEN)
            except posts.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
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
        try:
            k= CustomUser.objects.get(pk =request.data["user"])
            ser =  loginserializer(k)
            if str(request.user) == ser.data["first_name"]:
                if newpostserial.is_valid():
                    newpostserial.save()
                    return Response(newpostserial.data,status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
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
            ser = postserializer_byid(serial,data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data,status=status.HTTP_200_OK)
            print("invalid data",ser.error_messages)
            return Response(status= status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,*args,**kwargs):
        errors =False
        serial,errors = get_model_of_post(id,request)
        if errors == True:
            return serial
        
        serial.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        




'''
function that check if user is owner of the post and return serializer for read
'''
def get_seriallizer_of_post(id,request):
    try:
        postdata = posts.objects.get(pk=id)
        serial  =  postserializer_byid(postdata)
        print(serial.data)
        print("mine",serial.data["user"])
        userdata= CustomUser.objects.get(id = int(serial.data["user"]))
        try:
            userserial = loginserializer(userdata)
            if str(request.user) == userserial.data["first_name"]:
                return serial,False
            print("else")
            return Response(status=status.HTTP_403_FORBIDDEN),True
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND),True


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
        try:
            userserial = loginserializer(userdata)
            if str(request.user) == userserial.data["first_name"]:
                return postdata,False
            print("else")
            return Response(status=status.HTTP_403_FORBIDDEN),True
        except CustomUser.DoesNotExist:
            print("user not found")
            return Response(status=status.HTTP_404_NOT_FOUND),True

    except posts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND),True


'''
create a comment if you are logedin
'''

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def make_comment(request):
    if request.method == 'POST':
        newcommentserial = commentserializer(data= request.data)
        try:
            k= CustomUser.objects.get(pk =request.data["user"])
            ser =  loginserializer(k)
            
            if str(request.user) == ser.data["first_name"]:
                if newcommentserial.is_valid():
                    newcommentserial.save()
                pass
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


