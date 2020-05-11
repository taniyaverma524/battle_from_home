from django.urls import path , include
from apps.users.views import UserRegistrationApiView, UserUpdateApiView, LoginLogoutApiView ,UserChangePasswordApi\
    ,ForgotPasswordApi ,ResetPasswordApi
app_name = 'user'

urlpatterns = [

    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('updateuser/', UserUpdateApiView.as_view(), name='updateuser'),
    path('login/', LoginLogoutApiView.as_view(), name='login'),
    path('change-password/', UserChangePasswordApi.as_view(), name='change_password'),
    path('forgot-password/', ForgotPasswordApi.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordApi.as_view(), name='reset_password'),
]