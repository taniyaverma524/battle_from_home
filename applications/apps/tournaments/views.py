from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from apps.tournaments.models import Tournament
from apps.tournaments.serializer import TournamentTitleSerializer, TournamentSerializer, TournamentUserListSerializer
from rest_framework.response import Response
from apps.users.models import User


class GetTournamnetsApiView(APIView):
    def get(self, request, format=None):
        tournamnet_object=Tournament.objects.filter(active=True)
        tournamnet_serializer=TournamentTitleSerializer(tournamnet_object,many=True)
        user=request.user
        data={'tournament':tournamnet_serializer.data , 'user':user}

        return Response(tournamnet_serializer.data)


class GetDetailTournamentView(APIView):
    def get_object(self,pk):
        try:
            print(pk)
            return Tournament.objects.get(slug=pk,active=True)
        except  ObjectDoesNotExist:
            return Http404


    def get(self,request,pk):
        print(pk,'i am here')
        queryset=self.get_object(pk)
        serializer=TournamentSerializer(queryset)
        data={}
        base_url = request.get_host()
        image=Tournament.objects.get(slug=pk,active=True).bg_picture
        data['data']=serializer.data
        data['image']='http://'+base_url+ image
        return Response(data)



class GetTournamnetsListApiView(APIView):

    def get(self, request, name):
        name=name.replace('_'," ")
        tournamnet_object=Tournament.objects.filter(active=True,tournament_type=name)
        tournamnet_serializer=TournamentTitleSerializer(tournamnet_object,many=True)
        return Response(tournamnet_serializer.data)



class JoinEventApiView(APIView):
    def patch(self,request):
        print(request.user)
        user=request.user
        if user != 'AnonymousUser':
            # user=User.objects.get()
            print(request.user)
        return Response(
            {
                'message': 'Invalid credentials.',
                'data': {}
            },
            status=status.HTTP_401_UNAUTHORIZED)


class GetListJoinUserApiView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_list.html'
    def get(self,request,slug):
        print(slug)
        get_object=Tournament.objects.get(slug=slug)
        serializer=TournamentUserListSerializer(get_object)
        return Response({'data':serializer.data})
