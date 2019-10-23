import django_filters

from JJE_Standings.models import YahooStanding


class RankingFilter(django_filters.FilterSet):
    rank_gt = django_filters.NumberFilter(field_name="rank", lookup_expr='gt')
    rank_lt = django_filters.NumberFilter(field_name="rank", lookup_expr='lt')

    rank_gte = django_filters.NumberFilter(field_name="rank", lookup_expr='gte')
    rank_lte = django_filters.NumberFilter(field_name="rank", lookup_expr='lte')

    yahoo_team = django_filters.NumberFilter(field_name='yahoo_team')

    class Meta:
        model = YahooStanding
        fields = [
            'rank',
            'yahoo_team',
            # 'yahoo_team__id',
        ]


class AllRankFilter(django_filters.FilterSet):

    team_id_in = django_filters.CharFilter(field_name='team_id', lookup_expr='in')

    class Meta:
        fields = [
            'team_id',
        ]