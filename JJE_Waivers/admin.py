from django.contrib import admin
from .models import WaiverClaim, YahooTeam
from django.contrib.auth.admin import UserAdmin


class WaiverClaimAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fieldsets = [
        ('Claim ID',
         {'fields': ['id']}
         ),
        (None,
         {'fields': ['claim_start']}
         ),
        ('Team',
         {'fields': ['team']}
         ),
        ('Overclaim/Cancelled',
         {
             'fields': [
                 'overclaimed',
                 'over_claim_id',
                 'cancelled'
             ]
         }
         ),
        ('Add Player Info',
         {'fields': [
             'add_player',
             'add_LW',
             'add_C',
             'add_RW',
             'add_D',
             'add_G',
             'add_Util',
             'add_IR',
         ]}
         ),
        ('Drop Player Info', {'fields': [
            'drop_player',
            'drop_LW',
            'drop_C',
            'drop_RW',
            'drop_D',
            'drop_G',
            'drop_Util',
            'drop_IR',
        ]}),
    ]
    list_display = [
        'pk',
        'add_player',
        'drop_player',
        'team',
        'active_claim'
    ]


class YahooTeamAdmin(admin.ModelAdmin):
    list_display = [
        'team_name',
        'manager_name',
        'manager_email',
        'user'
    ]

admin.site.register(WaiverClaim, WaiverClaimAdmin)
admin.site.register(YahooTeam, YahooTeamAdmin)

UserAdmin.list_display = ('email', 'is_staff')
