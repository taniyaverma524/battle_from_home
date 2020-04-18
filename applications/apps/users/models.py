from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GenderChoices=(
        ('Male','Male'),
        ('Female','Female'),
        ('Transgender','Transgender'),
    )
    mobile = models.IntegerField(null=True, blank=True)
    gender= models.CharField(choices=GenderChoices,null=True,blank=True,max_length=20)
    dob= models.DateField(null=True,blank=True)
    profile_picture=models.CharField(max_length=200,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modifield_on=models.DateTimeField(auto_now=True)

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



