from JJE_Standings.models import YahooStanding

from django.conf import settings
from django.db import transaction

from django.contrib.sites.models import Site

from bs4 import BeautifulSoup
from datetime import datetime
import math
import requests
import os


def query_standings(token):
    site = Site.objects.first()

    url = os.path.join(site.domain, "oauth/api/getstandings/")
    url = url.replace("\\", "/")
    headers = {'Authorization': f'Token {token}'}
    res = requests.get(url, headers=headers, verify=settings.VERIFY_REQUEST)

    if res.status_code != 200:
        print("Error")
        print(res.text)
        return

    return res.json()


def query_team(token):
    site = Site.objects.first()

    url = os.path.join(site.domain, "api/teams/")
    url = url.replace("\\", "/")
    headers = {'Authorization': f'Token {token}'}
    res = requests.get(url, headers=headers, verify=settings.VERIFY_REQUEST)
    res_json = res.json()

    dc = {}
    for i in res_json:
        dc[i['team_id']] = {
            'id': i['id'],
            'team_name': i['team_name']
        }
    return dc


def update_standings(token):
    print(f"token {token}")

    yahoo_res = query_standings(token)

    if yahoo_res is None:
        # todo error logging here
        print("error")
        return False

    new_standings = yahoo_res['results']
    status_code = yahoo_res['status_code']

    teams = query_team(token)

    set_standings_not_current()

    process_new_standings(new_standings, teams)

    return True


def set_standings_not_current():
    for item in YahooStanding.objects.all():
        item.current_standings = False
        item.save()


@transaction.atomic
def process_new_standings(results, teams_json):
    standings_soup = BeautifulSoup(results, 'html.parser')

    team_list = []
    teams = standings_soup.findAll('team')
    for team in teams:
        team_obj = _process_team_row(team, teams_json)

        standings_class = _process_standings(
            team, team_obj
        )
    return team_list


def _process_team_row(team_row_xml, team_json):
    team_id = team_row_xml.find('team_id').text
    js = team_json[team_id]
    return js['id']


def _process_standings(team_row_xml, team_obj):
    standings_class = YahooStanding()

    standings_class.rank = _process_rank(team_row_xml)
    standings_class = _process_team_stats(standings_class, team_row_xml)
    standings_class = _process_team_points(standings_class, team_row_xml)

    starting_week = settings.STARTING_WEEK
    standings_class.standings_week = math.floor(
        ((datetime.utcnow() - starting_week).days / 7)
    )

    standings_class.current_standings = True

    standings_class.yahoo_team_id = team_obj
    standings_class.save()

    return standings_class


def _process_team_stats(standings_class=None, team_row_xml=None):
    stats_rows = team_row_xml.find('team_stats').find('stats')
    standings_class.stat_1 = _stat_value(
        stats_rows.find('stat_id', text="1"))
    standings_class.stat_2 = _stat_value(
        stats_rows.find('stat_id', text="2"))
    standings_class.stat_3 = _stat_value(
        stats_rows.find('stat_id', text="3"))
    standings_class.stat_4 = _stat_value(
        stats_rows.find('stat_id', text="4"))
    standings_class.stat_5 = _stat_value(
        stats_rows.find('stat_id', text="5"))
    standings_class.stat_8 = _stat_value(
        stats_rows.find('stat_id', text="8"))
    standings_class.stat_12 = _stat_value(
        stats_rows.find('stat_id', text="12"))
    standings_class.stat_31 = _stat_value(
        stats_rows.find('stat_id', text="31"))
    standings_class.stat_19 = _stat_value(
        stats_rows.find('stat_id', text="19"))
    standings_class.stat_22 = _stat_value(
        stats_rows.find('stat_id', text="22"))
    standings_class.stat_23 = _stat_value(
        stats_rows.find('stat_id', text="23"))
    standings_class.stat_25 = _stat_value(
        stats_rows.find('stat_id', text="25"))
    standings_class.stat_24 = _stat_value(
        stats_rows.find('stat_id', text="24"))
    standings_class.stat_26 = _stat_value(
        stats_rows.find('stat_id', text="26"))
    standings_class.stat_27 = _stat_value(
        stats_rows.find('stat_id', text="27"))
    return standings_class


def _process_team_points(standings_class=None, team_row_xml=None):
    points_row = team_row_xml.find('team_points')

    try:
        point_total = float(points_row.find('total').text)
    except:
        point_total = 0.0

    standings_class.stat_point_total = point_total
    stats_rows = points_row.find('stats')
    standings_class.stat_points_1 = _stat_value(
        stats_rows.find('stat_id', text="1"))
    standings_class.stat_points_2 = _stat_value(
        stats_rows.find('stat_id', text="2"))
    standings_class.stat_points_3 = _stat_value(
        stats_rows.find('stat_id', text="3"))
    standings_class.stat_points_4 = _stat_value(
        stats_rows.find('stat_id', text="4"))
    standings_class.stat_points_5 = _stat_value(
        stats_rows.find('stat_id', text="5"))
    standings_class.stat_points_8 = _stat_value(
        stats_rows.find('stat_id', text="8"))
    standings_class.stat_points_12 = _stat_value(
        stats_rows.find('stat_id', text="12"))
    standings_class.stat_points_31 = _stat_value(
        stats_rows.find('stat_id', text="31"))
    standings_class.stat_points_19 = _stat_value(
        stats_rows.find('stat_id', text="19"))
    standings_class.stat_points_22 = _stat_value(
        stats_rows.find('stat_id', text="22"))
    standings_class.stat_points_23 = _stat_value(
        stats_rows.find('stat_id', text="23"))
    standings_class.stat_points_25 = _stat_value(
        stats_rows.find('stat_id', text="25"))
    standings_class.stat_points_24 = _stat_value(
        stats_rows.find('stat_id', text="24"))
    standings_class.stat_points_26 = _stat_value(
        stats_rows.find('stat_id', text="26"))
    standings_class.stat_points_27 = _stat_value(
        stats_rows.find('stat_id', text="27"))
    return standings_class


def _process_rank(team_row):
    team_standings = team_row.find('team_standings')
    try:
        rank = float(team_standings.find("rank").text)
    except:
        rank = 0.0
    return rank


def _stat_value(stat_row):
    try:
        value = float(stat_row.parent.find('value').text)
    except:
        value = 0.0
    return value
