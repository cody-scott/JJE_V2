import django_filters
from django_filters.fields import Lookup

from JJE_Standings.models import YahooStanding


class ListFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value is None:
            return qs
        # a = qs[:2]
        # return a
        value_list = [int(i) for i in value.split(u',')]
        r = qs.filter(yahoo_team_id__in=value_list)
        return r


class RankingFilter(django_filters.FilterSet):
    rank_gt = django_filters.NumberFilter(field_name="rank", lookup_expr='gt')
    rank_lt = django_filters.NumberFilter(field_name="rank", lookup_expr='lt')

    rank_gte = django_filters.NumberFilter(field_name="rank", lookup_expr='gte')
    rank_lte = django_filters.NumberFilter(field_name="rank", lookup_expr='lte')

    # yahoo_team = django_filters.NumberFilter(field_name='yahoo_team')
    yahoo_team__in = ListFilter(field_name='yahoo_team_id', label="Yahoo Team In")
    # yahoo_team_id = django_filters.UUIDFilter(field_name='yahoo_team_id', lookup_expr='in')

    class Meta:
        model = YahooStanding
        fields = [
            'rank',
            # 'yahoo_team',
            'yahoo_team__in',
        ]


class AllRankFilter(django_filters.FilterSet):

    team_id_in = django_filters.CharFilter(field_name='team_id', lookup_expr='in')

    class Meta:
        fields = [
            'team_id',
        ]