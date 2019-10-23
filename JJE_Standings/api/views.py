from rest_framework import viewsets, permissions
from rest_framework.response import Response

from django.conf import settings
from django.contrib.sites.models import Site
import os
import requests


from JJE_Standings.api import serializer as api_serializer
from JJE_Standings.models import YahooStanding
from JJE_Standings.api import filters as api_filter

from JJE_Main.models import YahooTeam


class CurrentStandingsViewSet(viewsets.ReadOnlyModelViewSet):
    filter_class = api_filter.RankingFilter

    queryset = YahooStanding.objects.all()
    serializer_class = api_serializer.YahooRankSerializer

    def get_queryset(self):
        standings_active = YahooStanding.objects.filter(
            current_standings=True
        )
        return standings_active


# returns all standings for each team
class AllStandingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = YahooTeam.objects.all()
    serializer_class = api_serializer.YahooTeamAllStandingsSerializer

    def get_queryset(self):
        qs = YahooTeam.objects.all()

        return qs

    filterset_fields = (
        'team_name',
        'team_id',
    )
