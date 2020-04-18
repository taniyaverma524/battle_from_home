from django import forms
from apps.tournaments.models import Tournament
import os
import time
import random
from PIL import Image
from django.conf import settings



def make_dir(dirname):
    # import ipdb;ipdb.set_trace()
    """
    Creates new directory if not exists
    :param dirname: String
    :return: String
    """
    try:
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return dirname
    except Exception as e:

        raise e


def image_upload_handler(image_object, root_dir, filename=None, resize=False, dimension=(), extension='JPEG',
                         quality=100):
    return_value = False
    if image_object:
        file_name = filename if filename is not None else str(random.randint(10000, 10000000)) + '_' + str(
            int(time.time())) + '_' + image_object.name
        try:
            im = Image.open(image_object)
            if im.mode in ("RGBA", "P"):
                im = im.convert("RGB")
            if resize:
                if len(dimension) == 2:
                    im.bg_picture(dimension, Image.ANTIALIAS)
                else:
                    raise ValueError('Dimension is required, when resize is True.')
            im.save(root_dir + file_name, extension, quality=quality)
            return_value = file_name
        except Exception as e:
            raise e
    return return_value


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