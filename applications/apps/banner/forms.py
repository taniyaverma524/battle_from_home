from django import forms
from apps.banner.models import FrontPageBanner
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
                    im.banner_image(dimension, Image.ANTIALIAS)
                else:
                    raise ValueError('Dimension is required, when resize is True.')
            im.save(root_dir + file_name, extension, quality=quality)
            return_value = file_name
        except Exception as e:
            raise e
    return return_value


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