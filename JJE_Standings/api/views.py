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


# drop this when scheduling works
from rest_framework.decorators import api_view, permission_classes
from JJE_Standings.utils.yahoo_data import update_standings
from JJE_Standings.utils import standing_emails
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def get_new_standings_data(request):
    data = request.data

    token_id = data.get('token')

    token = get_object_or_404(Token, key=token_id)

    # this is to wake up the website if not running
    site = Site.objects.first()
    requests.get(site.domain, verify=settings.VERIFY_REQUEST)

    if update_standings(token) is True:
        standing_emails.send_standings_email()

    return Response("Good")
