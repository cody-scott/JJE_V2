from rest_framework import viewsets, permissions
from rest_framework.response import Response


from JJE_Standings.api import serializer
from JJE_Standings.models import YahooStanding, YahooGUID, YahooTeam


# Overall View for GUID -> yahoo team with standings as hyperlink
class YahooGUIDViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = YahooGUID.objects.all()
    serializer_class = serializer.YahooGUIDSerializer
    filterset_fields = ['yahoo_guid']

    permission_classes = [permissions.IsAuthenticated]


# Returns GUID -> teams with current weekly rank of that team
class YahooTeamGUIDViewSetCurrentWeek(viewsets.ReadOnlyModelViewSet):
    queryset = YahooGUID.objects.all()
    serializer_class = serializer.YahooCurrentGUIDSerializer

    filterset_fields = (
        'yahoo_guid',
    )

    permission_classes = [permissions.IsAuthenticated]

from JJE_Standings.api import filters as api_filter

class CurrentStandingsViewSet(viewsets.ReadOnlyModelViewSet):
    filter_class = api_filter.RankingFilter

    queryset = YahooStanding.objects.all()
    serializer_class = serializer.YahooRankSerializer

    def get_queryset(self):
        standings_active = YahooStanding.objects.filter(
            current_standings=True
        )

        return standings_active


# returns all standings for each team
class AllStandingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = YahooTeam.objects.all()
    serializer_class = serializer.YahooTeamAllStandingsSerializer

    def get_queryset(self):
        qs = YahooTeam.objects.all()

        return qs
    filterset_fields = (
        'team_name',
        'team_id',
    )


# this view returns the Team -> GUID (for reverse lookups)
class YahooTeamGUIDViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = YahooTeam.objects.all()
    serializer_class = serializer.YahooTeamtoGUID
    filterset_fields = (
        'team_name',
        'team_id',
    )

    permission_classes = [permissions.IsAuthenticated]
