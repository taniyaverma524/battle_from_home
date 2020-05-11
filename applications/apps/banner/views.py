from rest_framework.views import APIView
from apps.banner.models import Banner ,FrontPageBanner
from apps.banner.serializer import BannerSerializer ,DescriptionSerializer
from rest_framework.response import Response



class GetFrontPagelBannerApiView(APIView):
    def get(self, request, format=None):
        banner_object_1=Banner.objects.filter(is_active=True)
        banner_object = FrontPageBanner.objects.filter(main_theme=banner_object_1[0])
        banner_serializer=BannerSerializer(banner_object,many=True)
        image_data=[]
        base_url=request.get_host()
        print(request.user)
        for i in banner_serializer.data:
            image_data_dict = {}
            image_data_dict['banner_image']='http://'+base_url+ i.get('banner_image')
            image_data.append(image_data_dict)
        return Response(image_data)


class GetDescription(APIView):
    def get(self, request, format=None):
        description_object=Banner.objects.filter(is_active=True)[0]
        description_serializer=DescriptionSerializer(description_object)
        return Response(description_serializer.data)
