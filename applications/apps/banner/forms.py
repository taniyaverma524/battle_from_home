from django import forms
from apps.banner.models import FrontPageBanner
import random
from django.conf import settings
from libraries.Functions import make_dir, image_upload_handler

class FrontPageBannerForm(forms.ModelForm):


    select_bgimage = forms.FileField(required=False)



    class Meta:
        model = FrontPageBanner
        fields = "__all__"

    def save(self, commit=True):
        extra_field = self.cleaned_data.get('select_bgimage', None)
        if extra_field:

            rndm = random.randint(100000, 9999999)
            upload_dir = make_dir(
                settings.MEDIA_ROOT + settings.CUSTOM_DIRS.get('FRONT_BANNER_IMAGE_DIR') + '/' + str(
                    rndm) + '/'
            )
            file_name = image_upload_handler(extra_field, upload_dir)
            banner_image = settings.MEDIA_URL + settings.CUSTOM_DIRS.get(
                'FRONT_BANNER_IMAGE_DIR') + '/' + str(rndm) + '/' + file_name
            self.instance.banner_image = banner_image



        return super(FrontPageBannerForm, self).save(commit=commit)