"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from apps.users import urls as user_urls
from apps.tournaments import urls as tournament_urls
from apps.banner import urls as banner_urls
from rest_framework.authtoken import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include(user_urls,namespace='user')),
    path('tournament/',include(tournament_urls,namespace='tournament')),
    path('banner/',include(banner_urls,namespace='banner')),
    path('api-token-auth/',views.obtain_auth_token,name='api-token-auth'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)