from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from apps.users.forms import UserForm
from apps.users.models import User


def get_image_preview(obj):
    if obj.pk and obj.profile_picture :
        return mark_safe('<img src="%s" width="600" height="250" />' % (obj.profile_picture))
    return _("(choose a picture and save and continue editing to see the preview)")
get_image_preview.short_description=_("Picture Preview")

class UserAdmin(admin.ModelAdmin):
    form = UserForm
    readonly_fields = ['password',get_image_preview,'profile_picture']
    fieldsets = [
        ['User general information', {
            'fields': ['email',('first_name','last_name'),'password','mobile','gender','dob','profile_picture','select_profile_pic',get_image_preview,'date_joined','last_login']
        }],
        ['Account Details', {
            'fields': ['account_number','ifsc_code']
        }],
        ['Paytm Number', {
            'fields': ['paytm_number']
        }],
        ['UPI ID ', {
            'fields': ['upi_id']
        }],
        ['User permissions', {
            'classes': ['collapse'],
            'fields': ['user_permissions', 'groups', 'is_superuser', 'is_active', 'is_staff'],
        }],
    ]


admin.site.register(User,UserAdmin)
# Register your models here.
