from django.contrib import admin

# Register your models here.

from django.contrib import admin

from JJE_Main.models import YahooTeam, YahooGUID


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


admin.site.register(YahooTeam, TeamAdmin)
admin.site.register(YahooGUID, YahooGUIDAdmin)