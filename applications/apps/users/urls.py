from django.urls import path
from apps.users.views import UserRegistrationApiView ,UserUpdateApiView ,LoginLogoutApiView

app_name='users'

urlpatterns = [

    path('register/',UserRegistrationApiView.as_view(),name='register'),
    path('updateuser/<int:pk>/',UserUpdateApiView.as_view(),name='updateuser'),
    path('login/',LoginLogoutApiView.as_view(),name='login'),

]
