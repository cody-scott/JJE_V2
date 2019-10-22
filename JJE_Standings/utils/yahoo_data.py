from JJE_Standings.models import YahooStanding, YahooGUID, YahooTeam

from django.conf import settings

from django.contrib.sites.models import Site

from bs4 import BeautifulSoup
from datetime import datetime
import math
import requests


def update_standings(token):
    print(f"token {token}")

    site = Site.objects.first()

    url = site.domain + "oauth/api/getstandings/"
    headers = {'Authorization': f'Token {token}'}

    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print("Error")
        print(res.text)
        return

    yahoo_res = res.json()
    new_standings = yahoo_res['results']
    status_code = yahoo_res['status_code']

    set_standings_not_current()
    process_new_standings(new_standings)


def set_standings_not_current():
    for item in YahooStanding.objects.all():
        item.current_standings = False
        item.save()


def process_new_standings(results):
    standings_soup = BeautifulSoup(results, 'html.parser')
    team_list = league_standings(standings_soup)
    return True


def league_standings(xml_data=None):
    """
    Pass the xmlData in as a beautiful soup object
    team_list is a series of model objects that can be saved on return
    """
    team_list = []
    teams = xml_data.findAll('team')
    for team in teams:
        team_obj = _process_team_row(team)

        standings_class = _process_standings(
            team, team_obj
        )
    return team_list


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

    standings_class.yahoo_team = team_obj
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
