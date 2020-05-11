from django.contrib.auth import authenticate, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.users.models import User
from apps.users.serializer import RegisterUserSerializer ,UserUpdateSerializer
from rest_framework.views import APIView
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from libraries.Email_model import send_auth_email
from libraries.Email_templates import forgot_pwd_email_content
from libraries.Functions import get_unique_id


class UserRegistrationApiView(APIView):
    def post(self , request ,*args, **kwargs):
        if request.data['account_number']:
            serializer = RegisterUserSerializer(data=request.data,
                                                context={'confirm': request.data['confirm_password'],'confirm_account_number':request.data['confirm_account_number']})
        else:

            serializer = RegisterUserSerializer(data=request.data, context={'confirm': request.data['confirm_password']})
        if serializer.is_valid():
            reg_object = serializer.save()
            if reg_object:
                token= Token.objects.get(user=reg_object)
                return Response({
                    'status': status.HTTP_200_OK,
                        'message': 'You have been successfully logged in',
                        'data': {
                            'email': reg_object.email,
                            'name': reg_object.first_name,
                            'mobile': reg_object.mobile,
                            'first_name':reg_object.first_name,
                            'last_name':reg_object.last_name,
                            'gender':reg_object.gender,
                            'dob':reg_object.dob,
                            'token': token.key,
                        },
                }, status=status.HTTP_201_CREATED)
        error_details={}
        a=0
        for key , value in serializer.errors.items():
            error_details[str(a)]=str(value[0])
            a=a+1
        print( error_details)
        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': error_details
            }, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,request):
        try:
            pk=request.user.id
            return User.objects.get(id=pk)
        except  ObjectDoesNotExist:
            return Http404

    def get(self, request):
        serializer_object=self.get_object(request)
        serializer = UserUpdateSerializer(serializer_object)
        return Response(serializer.data, status= status.HTTP_200_OK)
    def patch(self, request):
        serializer_object=self.get_object(request)
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
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'You have been successfully logged in',
                        'data': {
                            'email': user.email,
                            'name': user.first_name,
                            'mobile': user.mobile,
                            'token': token.key,
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




class UserChangePasswordApi(APIView):
    permission_classes = [IsAuthenticated]
    """
    
    post:
        API for change password. Token is required.
    """

    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        email = request.user.email

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if old_password and new_password and confirm_password:
            user = User.objects.get(email=email)
            if user.check_password(old_password):
                if len(new_password) >= 8 and len(new_password) <= 15:
                    if new_password == confirm_password:
                        user.password = make_password(new_password)
                        user.save()
                        return Response(
                            {
                                'status': status.HTTP_200_OK,
                                'message': 'Password has been changed. Go for logout and login again.'
                            },
                            status=status.HTTP_200_OK)
                    else:
                        return Response(
                            {
                                'status': status.HTTP_400_BAD_REQUEST,
                                'message': 'New password and confirm password does not match'
                            }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(
                        {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'New password must be between 8 to 45 characters long'
                        }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid old password'
                    }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'old password, new password and confirm password are required fields'
                }, status=status.HTTP_400_BAD_REQUEST)



class ForgotPasswordApi(APIView):
    """
    post:
        API for send email for forgot password
    """


    def post(self, request):

        data = request.data
        email = data.get("email", None)
        if not email:
            return Response(
                {
                    "statu": status.HTTP_400_BAD_REQUEST,
                    "message": "Email parameter is required"
                }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except Exception:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    "message": "User not found with this email id"
                }, status=status.HTTP_400_BAD_REQUEST)

        pwd_reset_token = str(get_unique_id(user.id)).replace("-", "")
        user.password_reset_token = pwd_reset_token

        user.save()

        # Send Email
        subject = 'Battle-From-Home: Forgot password link'
        base_url = request.get_host()
        body = forgot_pwd_email_content(user, pwd_reset_token,base_url)
        received_user = user.email

        if send_auth_email(subject, body, received_user):
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "Password reset link sent on your registered email id"
                }, status=status.HTTP_200_OK)

        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Can not send the password reset link on your registered email. Please contact the battle from home team"
            }, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordApi(APIView):
    def post(self, request):

        data = request.data

        password_reset_token = data.get("reset_token", None)
        new_password = data.get("password", None)
        confirm_password = data.get("confirm_password", None)
        print( password_reset_token ,new_password ,confirm_password)

        if not password_reset_token or not new_password or not confirm_password:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Password, confirm password and password reset token are required fields"
                }, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "new password, confirm password must be same"
                }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(password_reset_token=password_reset_token)
        if len(user) == 0:

            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid password reset token"
                }, status=status.HTTP_400_BAD_REQUEST)

        user = user[0]

        user.password = make_password(new_password)
        user.password_reset_token = None

        user.save()

        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": "Password has been reset successfully. Please login to continue"
            }, status=status.HTTP_200_OK)

