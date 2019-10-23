from django.contrib import admin
from JJE_Standings.models import YahooStanding, YahooGUID, YahooTeam


class StandingsAdmin(admin.ModelAdmin):
    list_display = [
        'yahoo_team',
        'rank',
        'stat_point_total',
        'current_standings',
        'standings_week',
    ]
    ordering = ['-standings_week', 'rank']
    list_per_page = 12


class TeamAdmin(admin.ModelAdmin):
    readonly_fields = ('team_id', 'team_name', 'logo_url')
    fields = ('team_id', 'team_name', 'logo_url')
    list_display = [
        'team_name',
    ]


class YahooGUIDAdmin(admin.ModelAdmin):
    readonly_fields = ('manager_name', 'yahoo_guid')
    fields = ('manager_name', 'yahoo_guid', 'yahoo_team')

    list_display = [
        'manager_name',
        'yahoo_guid',
    ]


admin.site.register(YahooStanding, StandingsAdmin)
admin.site.register(YahooTeam, TeamAdmin)
admin.site.register(YahooGUID, YahooGUIDAdmin)
