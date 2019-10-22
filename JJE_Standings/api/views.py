from rest_framework import viewsets

from JJE_Standings.api import serializer
from JJE_Standings.models import YahooStanding, YahooGUID, YahooTeam


class YahooGUIDViewSet(viewsets.ModelViewSet):
    queryset = YahooGUID.objects.all()
    serializer_class = serializer.YahooGUIDSerializer
    filterset_fields = ['yahoo_guid']


class YahooTeamGUIDViewSetCurrentWeek(viewsets.ModelViewSet):
    queryset = YahooGUID.objects.all()
    serializer_class = serializer.YahooGUIDSerializer

    def get_queryset(self):
        return YahooGUID.objects.filter(
            yahoo_team__standings__current_standings=True
        )


# not returning as expected
class CurrentStandingsViewSet(viewsets.ModelViewSet):
    queryset = YahooStanding.objects.all()
    serializer_class = serializer.YahooRankSerializer

    def get_queryset(self):
        standings_active = YahooStanding.objects.filter(
            current_standings=True
        )
        return standings_active


class AllStandingsViewSet(viewsets.ModelViewSet):
    queryset = YahooStanding.objects.all()
    serializer_class = serializer.YahooRankSerializer


class YahooTeamGUIDViewSet(viewsets.ModelViewSet):
    queryset = YahooTeam.objects.all()
    serializer_class = serializer.YahooTeamtoGUID


