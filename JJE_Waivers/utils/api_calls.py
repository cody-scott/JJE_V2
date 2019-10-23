from django.conf import settings
from django.contrib.sites.models import Site

import requests
import os


def get_users_teams_waivers_request(request):
    auth_key = request.user.auth_token.key
    guid = request.user.usertoken_set.first().user_guid
    return get_users_teams_waivers(auth_key, guid)


def get_users_teams_waivers(auth_key, guid):
    site = Site.objects.first()
    headers = {'Authorization': f'Token {auth_key}'}
    url = os.path.join(site.domain, f"waivers/api/waivers_guid/?yahoo_guid={guid}")

    res = requests.get(url, headers=headers, verify=settings.VERIFY_REQUEST)

    team_list = []
    for r in res.json():
        for t in r.get('yahoo_team', []):
            team_list.append({'id': t['id'], 'team_id': t['team_id'], 'team_name': t['team_name']})

    return team_list


def get_overclaim_teams(request, team_list):
    # team_list is list of [{'team_id': X, 'team_name': Y}]

    id_list = ",".join([val['team_id'] for val in team_list])

    site = Site.objects.first()
    headers = {'Authorization': f'Token {request.user.auth_token.key}'}
    url = os.path.join(site.domain, f"standings/api/current_standings/?yahoo_team__team_id_in={id_list}")
    res = requests.get(url, headers=headers, verify=settings.VERIFY_REQUEST)

    lowest_team_rank = max([i.get('current_rank') for i in res.json()])
    url = os.path.join(site.domain, f"standings/api/current_standings/?rank_lt={lowest_team_rank}")
    res = requests.get(url, headers=headers, verify=settings.VERIFY_REQUEST)

    overclaim_teams = [t.get('team_id') for t in res.json()]
    return overclaim_teams
