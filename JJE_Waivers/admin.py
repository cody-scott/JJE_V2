from django.contrib import admin

from JJE_Waivers.models import WaiverClaim


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
         {'fields': ['yahoo_team']}
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
        'yahoo_team',
        'active_claim'
    ]


admin.site.register(WaiverClaim, WaiverClaimAdmin)

# UserAdmin.list_display = ('email', 'is_staff')
