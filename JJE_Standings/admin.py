from django.contrib import admin
from JJE_Standings.models import YahooStanding


class StandingsAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields if f.name not in ['current_standings']]

    list_display = [
        'yahoo_team',
        'rank',
        'stat_point_total',
        'current_standings',
        'standings_week',
    ]
    ordering = ['-standings_week', 'rank']
    list_per_page = 12


admin.site.register(YahooStanding, StandingsAdmin)

