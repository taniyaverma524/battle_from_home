from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from apps.tournaments.forms import TournamentForm
from apps.tournaments.models import Tournament
# Register your models here.


admin.site.index_title = 'Battle From Home Admin'
admin.site.site_header = 'Battle From Home'
admin.site.index_title = 'Battle From Home Administrator'



def get_image_preview(obj):
    if obj.pk and obj.bg_picture :
        return mark_safe('<img src="%s" width="600" height="250" />' % (obj.bg_picture))
    return _("(choose a picture and save and continue editing to see the preview)")
get_image_preview.short_description=_("Picture Preview")



class TournamentAdmin(admin.ModelAdmin):
    form=TournamentForm
    prepopulated_fields = {'slug': ('match_name',)}
    list_display = ['match_name','match_type','tournament_type','map','active','slot_occupancy']
    fields = [('match_name','slug'),'match_type','user_list',('tournament_type','map'),'date_of_match','winning_prize','slot_occupancy',('room_id','room_password')
        ,'per_kill','entry_fee','description','active','bg_picture','select_bgimage',get_image_preview]
    readonly_fields = ['bg_picture',get_image_preview,'slot_occupancy']
    radio_fields = {"match_type": admin.VERTICAL,"tournament_type":admin.VERTICAL}

admin.site.register(Tournament,TournamentAdmin)
