import django_filters

from JJE_Standings.models import YahooStanding


class RankingFilter(django_filters.FilterSet):
    rank_gt = django_filters.NumberFilter(field_name="rank", lookup_expr='gt')
    rank_lt = django_filters.NumberFilter(field_name="rank", lookup_expr='lt')

    rank_gte = django_filters.NumberFilter(field_name="rank", lookup_expr='gte')
    rank_lte = django_filters.NumberFilter(field_name="rank", lookup_expr='lte')

    yahoo_team__team_id_in = django_filters.CharFilter(field_name='yahoo_team__team_id', lookup_expr='in')

    class Meta:
        model = YahooStanding
        fields = [
            'rank',
            'yahoo_team__team_name',
            'yahoo_team__team_id',
        ]
