'''view for post'''
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from account.models import CustomUser
from account.serializer import LoginSerializer
from .models import comment, posts
from .serializer import PostSerializer, CreatePostSerializer
from .serializer import CommentGetSerialiser
from .task import sent_mail2

# Create your views here.


@api_view(['GET'])
def get_all_post(request):
    '''
    to get all post and comments
    '''
    if request.method == 'GET':
        postdata = posts.objects.all()
        postserial = PostSerializer(postdata, many=True)
        return Response(postserial.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_content(request):
    '''
    mycontent with userid and only content i created
    '''
    if request.method == 'GET':
        print(request.user)
        try:
            userdata = CustomUser.objects.get(first_name=request.user)
            userserial = LoginSerializer(userdata)
            # print("user id",userserial.data['id'])
            try:
                postdata = posts.objects.all().filter(user=int(userserial.data['id']))
                if str(request.user) == str(userserial.data["first_name"]):
                    postserial = PostSerializer(postdata, many=True)
                    return Response(postserial.data, status=status.HTTP_200_OK)
                return Response(status=status.HTTP_403_FORBIDDEN)
            except postdata.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except userdata.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)





@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_new_post(request):
    '''
    to create post if you are a logedin user
    '''
    if request.method == 'POST':
        newpostserial = CreatePostSerializer(data=request.data)
        try:
            userdata = CustomUser.objects.get(pk=request.data["user"])
            ser = LoginSerializer(userdata)
            if str(request.user) == ser.data["first_name"]:
                if newpostserial.is_valid():
                    newpostserial.save()
                    return Response(newpostserial.data,
                                    status=status.HTTP_201_CREATED)
                return Response(newpostserial.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except userdata.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class PostCrud(APIView):
    '''
    class to read , update ,delete post based  on post id
    '''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        '''post get '''
        errors = False
        serial ,errors = get_seriallizer_of_post(id, request)
        if errors is True:
            return serial
        return Response(serial.data)

    def put(self, request, id):
        '''post update'''
        errors = False
        serial , errors = get_model_of_post(id,request)
        if errors is True:
            return serial
        else :
            ser = CreatePostSerializer(serial, data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_200_OK)
            # print("invalid data",ser.error_messages)

            return Response(ser.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        '''post delete'''
        errors = False
        serial,errors = get_model_of_post(id, request)
        if errors is True:
            return serial

        serial.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





def get_seriallizer_of_post(id, request):
    '''
    function that check if user is owner of the post and return serializer for read
    '''
    try:
        postdata = posts.objects.get(pk=id)
        serial  =  CreatePostSerializer(postdata)
        # print(serial.data)
        # print("mine",serial.data["user"])
        userdata= CustomUser.objects.get(id = int(serial.data["user"]))
        try:
            userserial = LoginSerializer(userdata)
            if str(request.user) == userserial.data["first_name"]:
                return serial,False
            # print("else")
            return Response(status=status.HTTP_403_FORBIDDEN),True
        except userdata.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND),True


    except postdata.DoesNotExist:
        return Response("invalid post /post not found",status=status.HTTP_404_NOT_FOUND),True



def get_model_of_post(id,request):
    '''
    function to check if user is owner of the
    post and return model for put, delete
    '''
    try:
        postdata = posts.objects.get(pk=id)
        serial  =  CreatePostSerializer(postdata)
        try:
            userdata= CustomUser.objects.get(pk = serial.data["user"])
            userserial = LoginSerializer(userdata)
            if str(request.user) == userserial.data["first_name"]:
                return postdata,False
            # print("else")
            return Response(status=status.HTTP_403_FORBIDDEN),True
        except userdata.DoesNotExist:
            # print("user not found")
            return Response("user not found",status=status.HTTP_404_NOT_FOUND),True

    except postdata.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND),True




@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def make_comment(request):
    '''
    create a comment only  if you are logedin
    '''
    if request.method == 'POST':
        newcommentserial = CommentGetSerialiser(data= request.data)
        try:
            # print(request.data["created_by"])
            userobj= CustomUser.objects.get(pk=request.data["created_by"])
            ser =  LoginSerializer(userobj)
            try:
                # print(request.data["ofpost"])
                postobj = posts.objects.get(pk = request.data["ofpost"])
                postser = PostSerializer(postobj)
                if str(request.user) == str(ser.data["first_name"]):
                    if newcommentserial.is_valid():
                        newcommentserial.save()
                        sent_mail2.delay("A user comented on your post ",ser.data["email"])
                        # test("user comented on your post ",ser.data["email"])
                        # if(res == "Done"):
                        return Response(newcommentserial.data,status=status.HTTP_200_OK)
                    # print(newcommentserial.error_messages)
                # print("199")
                return Response( "user not atorized",  status=status.HTTP_403_FORBIDDEN)
            except postobj.DoesNotExist:
                return Response(postser.errors,status=status.HTTP_404_NOT_FOUND)
        except userobj.DoesNotExist:
            return Response(ser.errors, status=status.HTTP_404_NOT_FOUND)




class CommentsClass(APIView):
    '''
    comment class to get update and delete
    comment by the on who created it
    '''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        '''get commnet one'''
        errors = False
        serial ,errors = get_serializer_of_commnet(id,request)
        if errors is True:
            return serial
        return Response(serial.data,status=status.HTTP_200_OK)

    def put(self, request ,id):
        '''update comment'''
        errors = False
        serial , errors = get_model_of_comment(id,request)
        if errors is True:
            return serial
        else :
            ser = CommentGetSerialiser(serial,data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data,status=status.HTTP_200_OK)
            # print("invalid data",ser.error_messages)
            return Response(ser.errors,status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        '''delete comment'''
        errors = False
        serial , errors = get_model_of_comment(id,request)
        if errors is True:
            return serial

        serial.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def get_serializer_of_commnet(id, request):
    '''
    function that return commnet serializer if the
    user is autheorized
    '''
    try:
        commnetdata = comment.objects.get(pk = id)
        serial = CommentGetSerialiser(commnetdata)
        try:
            userobj = CustomUser.objects.get(id = int(serial.data["created_by"]))
            userserial  = LoginSerializer(userobj)
            if str(request.user) == userserial.data["first_name"]:
                return serial,False
                # print("else")
            return Response(status=status.HTTP_403_FORBIDDEN), True
        except userobj.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND), True
    except commnetdata.DoesNotExist:
        logging.warning(f"comment  not found of id{id}")
        return Response("comment  not found",status=status.HTTP_404_NOT_FOUND), True

def get_model_of_comment(id, request):
    '''
    function return model of comment if
    the user is autheorized
    '''
    try:
        commenttdata = comment.objects.get(pk=id)
        serial  =  CommentGetSerialiser(commenttdata)
        try:
            userdata= CustomUser.objects.get(pk = serial.data["created_by"])
            userserial = LoginSerializer(userdata)
            if str(request.user) == userserial.data["first_name"]:
                return commenttdata,False
            # print("else")
            return Response(status=status.HTTP_403_FORBIDDEN), True
        except userdata.DoesNotExist:
            # print("user not found")
            return Response(status=status.HTTP_404_NOT_FOUND), True

    except commenttdata.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND), True
        