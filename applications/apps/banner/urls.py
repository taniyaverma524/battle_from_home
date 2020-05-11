from django.urls import path
from apps.banner.views import GetFrontPagelBannerApiView ,GetDescription

app_name='banner'

urlpatterns = [

    path('frontpagebanner/',GetFrontPagelBannerApiView.as_view(),name='frontpage-banner'),
    path('frontpagedescription/',GetDescription.as_view(),name='frontpagedescription'),


]
