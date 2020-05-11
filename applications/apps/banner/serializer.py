from rest_framework import serializers
from apps.banner.models import Banner ,FrontPageBanner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=FrontPageBanner
        fields = ['banner_image']




class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banner
        fields = ['description']



