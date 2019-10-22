import django_filters

from JJE_Standings.models import YahooStanding


class RankingFilter(django_filters.FilterSet):
    rank_gte = django_filters.NumberFilter(field_name="rank", lookup_expr='gt')

    class Meta:
        model = YahooStanding
        fields = [
            'rank',
            'yahoo_team__team_name',
            'yahoo_team__team_id',
        ]
