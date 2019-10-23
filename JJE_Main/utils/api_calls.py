from django.conf import settings
from django.contrib.sites.models import Site

from JJE_Main.models import YahooGUID, YahooTeam

from bs4 import BeautifulSoup
from datetime import datetime
import math
import requests
import os


def update_teams(request):
    site = Site.objects.first()

    url = os.path.join(site.domain, "oauth/api/getteams/")
    url = url.replace("\\", "/")
    headers = {'Authorization': f'Token {request.user.auth_token.key}'}

    res = requests.get(url, headers=headers, verify=settings.VERIFY_REQUEST)

    yahoo_res = res.json()
    team_xml = yahoo_res['results']
    status_code = yahoo_res['status_code']

    team_xml = BeautifulSoup(team_xml, 'html.parser')
    teams = team_xml.find_all('team')
    for team in teams:
        team_obj = _process_team_row(team)

    return res


def _process_team_row(team_row_xml):
    team_id = team_row_xml.find('team_id').text
    team_name = team_row_xml.find('name').text
    managers = _get_managers(team_row_xml)

    team_class = YahooTeam.objects.filter(team_id=team_id).first()
    if team_class is None:
        team_class = YahooTeam()
    team_class.team_id = team_row_xml.find('team_id').text
    team_class.team_name = team_row_xml.find('name').text
    team_class.logo_url = team_row_xml.find('team_logo').find('url').text
    team_class.save()

    for manager in managers:
        manager.yahoo_team.add(team_class)

    return team_class


def _get_managers(team_row_xml):
    guid_objects = []
    for manager in team_row_xml.findAll('manager'):
        manager_guid = manager.find('guid').text
        manager_name = manager.find('nickname').text

        guid_obj = YahooGUID.objects.filter(yahoo_guid__contains=manager_guid)
        if len(guid_obj) == 0:
            guid_obj = YahooGUID()
            guid_obj.yahoo_guid = manager_guid
            guid_obj.manager_name = manager_name
            guid_obj.save()
        else:
            guid_obj = guid_obj[0]
        guid_objects.append(guid_obj)
    return guid_objects
