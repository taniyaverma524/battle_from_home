from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from config import settings


class User(AbstractUser):
    GenderChoices=(
        ('Male','Male'),
        ('Female','Female'),
        ('Transgender','Transgender'),
    )
    mobile = models.CharField(null=True, blank=True,max_length=20)
    gender= models.CharField(choices=GenderChoices,null=True,blank=True,max_length=20)
    dob= models.DateField(null=True,blank=True)
    profile_picture=models.CharField(max_length=200,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modifield_on=models.DateTimeField(auto_now=True)
    account_number=models.CharField(null=True,blank=True,max_length=100)
    ifsc_code=models.CharField(null=True,blank=True,max_length=50)
    password_reset_token = models.CharField(max_length=100, null=True, blank=True)
    upi_id=models.CharField(null=True,blank=True,max_length=100)
    paytm_number=models.CharField(null=True, blank=True,max_length=20)
    class Meta:
         db_table='auth_user'
         default_permissions = ()
         permissions = (
             # Users related permissions
             ('view_user', 'Can view users.'),
             ('list_user', 'Can list users.'),
             ('add_user', 'Can add users.'),
             ('edit_user', 'Can edit users.'),
             ('delete_user', 'Can delete users.'),
             ('csv_for_user', 'Can download csv for users.'),

             # More Permissions
         )


@receiver(post_save ,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None, created=False , **kwargs):
    if created:
        Token.objects.create(user=instance)

