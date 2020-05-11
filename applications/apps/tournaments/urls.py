from django.urls import path
from apps.tournaments.views import GetTournamnetsApiView ,GetDetailTournamentView , GetTournamnetsListApiView\
    ,JoinEventApiView ,GetListJoinUserApiView

app_name='tournament'

urlpatterns = [
    path('all-tournament/',GetTournamnetsApiView.as_view(),name='all-tournament'),
    path('detail-tournament/<str:pk>/', GetDetailTournamentView.as_view(), name='detail-tournament'),
    path('tournament_list/<str:name>/',GetTournamnetsListApiView.as_view(),name='list_tournament'),
    path('join_event/',JoinEventApiView.as_view(),name='list_tournament'),
    path('user_list/<str:slug>/',GetListJoinUserApiView.as_view(),name='user_list'),
]
