from rest_framework import serializers
from apps.tournaments.models import Tournament

class TournamentTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tournament
        fields = ['match_name','tournament_type','slug']


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tournament
        fields = ['match_name','match_type','tournament_type','map','date_of_match','winning_prize','per_kill','entry_fee','description','user_list','room_id','room_password']



class TournamentUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tournament
        fields = ['match_name','match_type','tournament_type','map','date_of_match','winning_prize','per_kill','entry_fee','description','user_list','room_id','room_password']
