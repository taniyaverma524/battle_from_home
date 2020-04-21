from apps.users.models import User
class EmailOrPhoneModelBackend(object):

    def authenticate(self,request, username=None, password=None):
        try:
            if '@' in username:

                kwargs = {'email': username}
                user = User.objects.get(**kwargs)
            elif username.isdigit():

                kwargs = {'mobile': username}
                user = User.objects.get(**kwargs)

            else:

                kwargs= {'username': username}
                user = User.objects.get(**kwargs)


        except User.MultipleObjectsReturned:
            user=User.objects.filter(**kwargs).order_by('id').first()
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user

        return None
    def get_user(self, user_id):
        try:

            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
