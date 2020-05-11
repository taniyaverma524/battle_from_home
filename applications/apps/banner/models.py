from django.db import models

# Create your models here.
class Banner(models.Model):
    theme_name=models.CharField(max_length=150,blank=True,null=True,unique=True)
    is_active = models.BooleanField(default=True,blank=True,null=True)
    description = models.TextField(max_length=300,blank=True,null=True)

    def __str__(self):
        return self.theme_name

class FrontPageBanner(models.Model):
    main_theme=models.ForeignKey(Banner,on_delete=models.CASCADE,related_name='main_theme')
    banner_image=models.CharField(max_length=500,blank=True,null=True)
