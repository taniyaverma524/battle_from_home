from django.contrib.auth import authenticate, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from apps.users.models import User
from apps.users.serializer import RegisterUserSerializer ,UserUpdateSerializer
from rest_framework.views import APIView
from django.contrib.auth import login as auth_login





class UserRegistrationApiView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self , request ,*args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data, context={'confirm': request.data['confirm_password']})
        if serializer.is_valid():
            reg_object = serializer.save()
            if reg_object:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateApiView(APIView):
    # permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            print(User.objects.get(id=pk),'tttttttttttttt')
            return User.objects.get(id=pk)
        except  ObjectDoesNotExist:
            return Http404

    def get(self, request,pk):
        serializer_object=self.get_object(pk)

        serializer = UserUpdateSerializer(serializer_object)
        return Response(serializer.data, status= status.HTTP_200_OK)
    def patch(self, request,pk):
        serializer_object=self.get_object(pk)
        print(request.data)
        serializer = UserUpdateSerializer(serializer_object,data=request.data,partial=True)
        if serializer.is_valid():
            user=serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        serializer_object=self.get_object(pk)
        serializer_object.delete()
        return Response(status=status.HTTP_200_OK)

class LoginLogoutApiView(APIView):
    def post(self,request):
        username=request.data.get('username',None)
        password=request.data.get('password',None)
        if username and password :
            user= authenticate(username=username,password=password)
            if user :
                auth_login(request, user)
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'You have been successfully logged in',
                        'data': {
                            'username': user.username,
                            'email': user.email,
                            'name': user.first_name
                        },
                    },
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        'message': 'Invalid credentials.',
                        'data': {}
                    },
                    status=status.HTTP_401_UNAUTHORIZED)

    def get(self,request):
        logout(request)
        return Response({
            'message': "you are successfully logout",
            'status': status.HTTP_200_OK
        }
            , status=status.HTTP_200_OK
        )





