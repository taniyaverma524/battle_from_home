from django.db import models
from apps.users.models import User

# Create your models here.
class Tournament(models.Model):
    MATCH_TYPE_CHOICES=(
        ('Solo','Solo'),
        ('Duo','Duo'),
        ('Squad','Squad'),
    )
    TOURNAMENT_TYPE_CHOICES=(
        ('PUBG Mobile','PUBG Mobile'),
        ('PUBG Mobile Lite', 'PUBG Mobile Lite'),
    )
    MAP_CHOICES=(
        ('PUBG MOBILE',(
             ('Erangle','Erangle'),
             ('Sanhok','Sanhok'),
             ('Miramer','Miramer'),
             ('Vikendi','Vikendi'),
             ('TDM : Warehouse','TDM : Warehouse'),
             )
             ),
        ('PUBG MOBILE LITE', (
            ('Varenge', 'Varenge'),
            ('Golden', 'Woods'),
            ('TDM : Warehouse', 'TDM : Warehouse'),
        )
         ),
    )
    match_name=models.CharField(max_length=150,unique=True,blank=True,null=True)
    slug=models.SlugField(max_length=150,unique=True,blank=True,null=True)
    match_type=models.CharField(max_length=50,choices=MATCH_TYPE_CHOICES,blank=True,null=True)
    tournament_type=models.CharField(max_length=50,choices=TOURNAMENT_TYPE_CHOICES,blank=True,null=True)
    map = models.CharField(max_length=100,choices=MAP_CHOICES,blank=True,null=True)
    date_of_match=models.DateTimeField(blank=True,null=True)
    winning_prize=models.IntegerField(blank=True,null=True)
    per_kill=models.IntegerField(blank=True,null=True)
    entry_fee=models.IntegerField(blank=True,null=True)
    description=models.TextField(max_length=250,blank=True,null=True)
    user_list=models.ManyToManyField(User,related_name='user_lists',blank=True)
    active=models.BooleanField(default=True,null=True,blank=True)
    bg_picture=models.CharField(max_length=250,null=True,blank=True)
    slot_occupancy=models.BooleanField(default=True,null=True,blank=True)
    room_id=models.CharField(max_length=50,null=True,blank=True)
    room_password=models.CharField(max_length=50,null=True,blank=True)


    def __str__(self):
        return self.match_name