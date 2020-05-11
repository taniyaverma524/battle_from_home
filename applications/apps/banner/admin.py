from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from apps.banner.models import Banner ,FrontPageBanner
from apps.banner.forms import FrontPageBannerForm



def get_image_preview(obj):
    if obj.pk and obj.banner_image :
        return mark_safe('<img src="%s" width="600" height="250" />' % (obj.banner_image))
    return _("(choose a picture and save and continue editing to see the preview)")
get_image_preview.short_description=_("Picture Preview")


class FrontPageBannerAdmin(admin.TabularInline):
    form=FrontPageBannerForm
    model = FrontPageBanner
    extra=1
    fields = ['banner_image','select_bgimage',get_image_preview]
    readonly_fields = [get_image_preview,'banner_image']


class BannerAdmin(admin.ModelAdmin):
    list_filter = ['is_active']
    search_fields = ['theme_name']
    list_display = ['theme_name','is_active']
    inlines = [FrontPageBannerAdmin]


admin.site.register(Banner,BannerAdmin)