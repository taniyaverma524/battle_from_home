import base64
import json
import  os, time
from PIL import Image
import  random, uuid
from datetime import datetime
from apps.users.models import User

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



def get_unique_id(id=None):
    return uuid.uuid5(uuid.NAMESPACE_DNS, str(id) + str(datetime.now()))



def is_email_exist(email):
    try:
        user = User.objects.get(email=email)
    except Exception:
        user = None
    return user




def base64encode(user):
    dict = {}
    dict['token'] = user.password_reset_token
    dict['name'] = user.first_name
    dict['username'] = user.last_name
    # dict['avatar'] = user.avatar

    dict = json.dumps(dict)
    encoded_dict = str(dict).encode('utf-8')
    base64_dict = base64.b64encode(encoded_dict)
    base64_dict_str = (str(base64_dict)).split("'")[1]
    return base64_dict_str
