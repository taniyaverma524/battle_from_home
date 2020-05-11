from django import forms
from apps.tournaments.models import Tournament
import random
from django.conf import settings

from libraries.Functions import make_dir, image_upload_handler


class TournamentForm(forms.ModelForm):


    select_bgimage = forms.FileField(required=False)



    class Meta:
        model = Tournament
        fields = "__all__"


    def clean_slot_occupancy(self):
        list_of_user=self.cleaned_data['user_list']
        match_type=self.cleaned_data['tournament_type']
        slot_occupancy=self.cleaned_data['slot_occupancy']
        count=len(list_of_user)
        if match_type == 'PUBG Mobile' and count == 100 :
            slot_occupancy=False
        elif match_type == 'PUBG Mobile Lite' and count == 60 :
            slot_occupancy = False
        else:
            slot_occupancy=True
        return slot_occupancy


    def save(self, commit=True):
        extra_field = self.cleaned_data.get('select_bgimage', None)
        if extra_field:

            rndm = random.randint(100000, 9999999)
            upload_dir = make_dir(
                settings.MEDIA_ROOT + settings.CUSTOM_DIRS.get('BG_IMAGE_DIR') + '/' + str(
                    rndm) + '/'
            )
            file_name = image_upload_handler(extra_field, upload_dir)
            bg_picture = settings.MEDIA_URL + settings.CUSTOM_DIRS.get(
                'BG_IMAGE_DIR') + '/' + str(rndm) + '/' + file_name
            self.instance.bg_picture = bg_picture



        return super(TournamentForm, self).save(commit=commit)