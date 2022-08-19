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
        '''login'''
        try:
            user_datas= CustomUser.objects.get(
                email= request.data['email'],
            password = request.data['password']
            )
        except user_datas.DoesNotExist:
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
        '''create user'''
        logz.info("get user data to creaet user")
        serial = LoginSerializer(data=request.data)
        if serial.is_valid():
            logz.info("data set and saved responded")
            serial.save()
            return Response(status=status.HTTP_200_OK)
        logz.warning("bad data error")
        return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)

class UserCrud(APIView):
    '''view is used for user to update delete  or update there
    account details '''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        ''' function to return user data'''
        logz.info("get user data")
        error=False
        serial,error = get_userobj_byid_and_avalicheck(id, request)
        if error is True:
            logz.warning("user data error")
            return serial
        logz.info("get user data sent")
        return Response(serial.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        '''update user data'''
        errors = False
        user_datas,errors= get_usermodel_byid_and_avalicheck(id, request)
        logz.info("get user data")
        if errors is False:
            serial = LoginSerializer(user_datas, data=request.data)
            if serial.is_valid():
                serial.save()
                logz.info("get user data updated")
                return Response(serial.data, status=status.HTTP_202_ACCEPTED)
            return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
        return user_datas

    def delete(self, request, id):
        '''delete user'''
        errors = False
        user_datas , errors= get_usermodel_byid_and_avalicheck(id, request)
        logz.info("get user data")
        if errors is False:
            user_datas.delete()
            logz.info("get user data deleted")
            return Response(status=status.HTTP_204_NO_CONTENT)
        return user_datas

def get_usermodel_byid_and_avalicheck(id, request):
    '''function used to return model '''

    try:
        user_datas= CustomUser.objects.get(pk=id)
        serial = LoginSerializer(user_datas)
        if str(request.user) == str(serial.data["first_name"]):
            return user_datas, False
        logz.warning("un authorized")
        return Response(status=status.HTTP_403_FORBIDDEN), True

    except user_datas.DoesNotExist:
        logz.warning("user not found")
        return Response("User not found", status=status.HTTP_404_NOT_FOUND), True




def get_userobj_byid_and_avalicheck(id, request):
    '''function used to return seializer '''

    try:
        user_datas= CustomUser.objects.get(pk=id)
        serial = LoginSerializer(user_datas)
        if str(request.user) == str(serial.data["first_name"]):
            return serial, False
        return Response(status=status.HTTP_403_FORBIDDEN), True

    except user_datas.DoesNotExist:
        logz.warning("user not found")
        return Response("User not found", status=status.HTTP_404_NOT_FOUND), True



@api_view(['GET','POST'])
def test_auth(request):
    '''simple test view'''
    if request.method == 'GET':
        res = adding_task(6,2)
        print(request.user)
        return Response(res, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
