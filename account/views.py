'''user view'''
import logging as logz
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from account.serializer import LoginSerializer
from .task import adding_task
from .models import CustomUser


# Create your views here.




class CustomAuthToken(ObtainAuthToken):
    '''custom login class which has post method that
         takes in email and password an return or create user token
     for login and return token as well as id'''

    def post(self, request):
        try:
            logz.info("user token access")
            user_datas= CustomUser.objects.get(
                email= request.data['email'],
            password = request.data['password']
            )
        except CustomUser.DoesNotExist:
            logz.warning("user not found ")
            # print("user not found")
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LoginSerializer(user_datas)
        logz.info("serializing data")
        token, created = Token.objects.get_or_create(user=user_datas)
        logz.info("token created or get and sent")
        data= {
            'token': token.key,
            'user_id':serializer.data["id"]
        }
        return Response(status=status.HTTP_200_OK,data=data)


class UserRegister(APIView):
    '''this view is used to register and create a new user
     only if data is valid'''
    def post(self, request):
        logz.info("get user data to creaet user")
        serial = LoginSerializer(data=request.data)
        if serial.is_valid():
            logz.info("data set and saved responded")
            serial.save()
            return Response(status=status.HTTP_200_OK)
        logz.warning("bad data error")
        return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)

class UserCrud(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    '''view is used for user to update delete  or update there 
    account details '''
    def get(self, request, id):
        logz.info("get user data")
        # print(request.user)
        error=False
        serial,error = get_userobj_byid_and_avalicheck(id, request)
        if error == True:
            logz.warning("user data error")
            return serial
        logz.info("get user data sent")
        return Response(serial.data, status=status.HTTP_200_OK)
        
    

    def put(self, request, id):
        user_datas= CustomUser.objects.get(pk=id)
        logz.info("get user data")
        serial = LoginSerializer(user_datas, data=request.data)
        # print(serial.is_valid())
        if serial.is_valid():
            serial.save()
            logz.info("get user data updated")
            return Response(serial.data, status=status.HTTP_202_ACCEPTED)
        return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            user_datas= CustomUser.objects.get(pk=id)
            logz.info("get user data")
            serial = LoginSerializer(user_datas)
            # print(serial.data)
            # print()
            if str(request.user) == str(serial.data["first_name"]):
                user_datas.delete()
                logz.info("get user data deleted")

                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                # print('else')
                logz.warning("data error")
                return Response(status=status.HTTP_403_FORBIDDEN)
        except CustomUser.DoesNotExist:
            # print("user not found")
            logz.warning("data error")
            return Response(status=status.HTTP_404_NOT_FOUND)


def get_userobj_byid(id, request):
    '''function to get object  by id and check if
        the user is the same my useing request.'''
    try:
        user_datas= CustomUser.objects.get(pk=id)
        serial = LoginSerializer(user_datas)
        # print(serial.data)
        if str(request.user) == str(serial.data["first_name"]):
            return user_datas, False
            
        return Response(status=status.HTTP_403_FORBIDDEN), True
    except CustomUser.DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND), True

def get_userobj_byid_and_avalicheck(id, request):
    '''function used to return seializer '''

    try:
        user_datas= CustomUser.objects.get(pk=id)
        serial = LoginSerializer(user_datas)
        if str(request.user) == str(serial.data["first_name"]):
            return serial, False

        return Response(status=status.HTTP_403_FORBIDDEN), True
        
    except CustomUser.DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND), True



@api_view(['GET','POST'])
def test_auth(request):
    '''simple test view'''
    if request.method == 'GET':
        res = adding_task(6,2)
        print(request.user)
        return Response(res, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)