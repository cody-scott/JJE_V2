from rest_framework import viewsets

from JJE_Standings.api import serializer
from JJE_Standings.models import YahooStanding, YahooGUID


class StandingsViewSet(viewsets.ModelViewSet):
    queryset = YahooStanding.objects.all()
    serializer_class = serializer.YahooStandingSerializer


class ActiveStandingsViewSet(viewsets.ModelViewSet):
    queryset = YahooStanding.objects.all()
    serializer_class = serializer.YahooStandingSerializer

    def get_queryset(self):
        standings_active = YahooStanding.objects.filter(
            current_standings=True
        )
        return standings_active


class YahooGUIDViewSet(viewsets.ModelViewSet):
    queryset = YahooGUID.objects.all()
    serializer_class = serializer.YahooGUIDSerializer
    filterset_fields = ['yahoo_guid']
