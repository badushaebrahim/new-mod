from pstats import Stats
from django.shortcuts import render
from account.serializer import loginserializer,updateserializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from celery import current_app
from .task import adding_task

import logging as logz
# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import CustomUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
class CustomAuthToken(ObtainAuthToken):


    def post(self, request, *args, **kwargs):
        try:
            logz.info("user token access")
            userdatas= CustomUser.objects.get(
                email= request.data['email'],
            password = request.data['password']
            )
        except CustomUser.DoesNotExist:
            logz.warning("user not found ")
            print("user not found")
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = loginserializer(userdatas)
        logz.info("serializing data")
        token, created = Token.objects.get_or_create(user=userdatas)
        logz.info("token created or get and sent")
        data= {
            'token': token.key,
            'user_id':serializer.data["id"]
        }
        return Response(status=status.HTTP_200_OK,data=data)


class user_Register(APIView):
    def post(self,request, *args, **kwargs):
        logz.info("get user data to creaet user")
        serial = loginserializer(data=request.data)
        if serial.is_valid():
            logz.info("data set and saved responded")
            serial.save()
            return Response(status=status.HTTP_200_OK)
        logz.warning("bad data error")
        return Response(status=status.HTTP_400_BAD_REQUEST)

class user_crud(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,id,*args,**kwargs):
        logz.info("get user data")
        # print(request.user)
        error=False
        serial,error = get_userobj_byid_and_avalicheck(id,request)
        if error == True:
            logz.warning("user data error")
            return serial
        logz.info("get user data sent")
        return Response(serial.data,status=status.HTTP_200_OK)
        
    

    def put(self,request,id,*args,**kwargs):
        userdatas= CustomUser.objects.get(pk=id)
        logz.info("get user data")
        serial = loginserializer(userdatas,data=request.data)
        print(serial.is_valid())
        if serial.is_valid():
            serial.save()
            logz.info("get user data updated")
            return Response(serial.data,status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id,*args,**kwargs):
        try:
            userdatas= CustomUser.objects.get(pk=id)
            logz.info("get user data")
            serial = loginserializer(userdatas)
            # print(serial.data)
            # print()
            if str(request.user) == str(serial.data["first_name"]):
                userdatas.delete()
                logz.info("get user data deleted")

                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                print('else')
                logz.warning("data error")
                return Response(status=status.HTTP_403_FORBIDDEN)
        except CustomUser.DoesNotExist:
            print("user not found")
            logz.warning("data error")
            return Response(status=status.HTTP_404_NOT_FOUND)


    



# function to get object  by id and check if the user is the same my useing request.

def get_userobj_byid(id,request):
    try:
        userdatas= CustomUser.objects.get(pk=id)
        serial = loginserializer(userdatas)
        # print(serial.data)
        if str(request.user) == str(serial.data["first_name"]):
            return userdatas,False
        else:
            print('else')
            Response(status=status.HTTP_403_FORBIDDEN)
            return Response(status=status.HTTP_403_FORBIDDEN),True
    except CustomUser.DoesNotExist:
            print("user not found")
            return Response(status=status.HTTP_404_NOT_FOUND),True
    

def get_userobj_byid_and_avalicheck(id,request):

    try:
        userdatas= CustomUser.objects.get(pk=id)
        serial = loginserializer(userdatas)
        print("req",request.user)
        print("ser",serial.data["username"])
        if str(request.user) == str(serial.data["first_name"]):
            return serial,False
        else:
            print('else')
            return Response(status=status.HTTP_403_FORBIDDEN),True
        
    except CustomUser.DoesNotExist:
            print("user not found")
            return Response(status=status.HTTP_404_NOT_FOUND),True



@api_view(['GET','POST'])
def test_auth(request):
    if request.method == 'GET':
        res = adding_task(6,2)
        return Response(res,status=status.HTTP_200_OK)