from django.contrib import admin

# Register your models here.
from JJE_Standings.models import YahooStanding


class StandingsAdmin(admin.ModelAdmin):
    list_display = [
        'team_name',
        'rank',
        'stat_point_total',
        'current_standings',
        'standings_week'
    ]
    ordering = ['-standings_week', 'rank']
    list_per_page = 12


admin.site.register(YahooStanding, StandingsAdmin)
