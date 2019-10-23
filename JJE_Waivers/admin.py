from django.contrib import admin

from JJE_Waivers.models import YahooTeam, YahooGUID, WaiverClaim


class TeamAdmin(admin.ModelAdmin):
    readonly_fields = ('team_id', 'team_name', 'logo_url')
    fields = ('team_id', 'team_name', 'logo_url')
    list_display = [
        'team_name',
    ]


class YahooGUIDAdmin(admin.ModelAdmin):
    readonly_fields = ('manager_name', 'yahoo_guid',)
    fields = ('manager_name', 'yahoo_guid', 'yahoo_team')

    list_display = [
        'manager_name',
        'yahoo_guid',
    ]

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


admin.site.register(YahooTeam, TeamAdmin)
admin.site.register(YahooGUID, YahooGUIDAdmin)
admin.site.register(WaiverClaim, WaiverClaimAdmin)

# UserAdmin.list_display = ('email', 'is_staff')
