from JJE_Standings.models import YahooStanding, YahooGUID

from Yahoo_Authentication.utils.oauth_flow import refresh_user_token, create_oauth_session
from Yahoo_Authentication.models import UserToken

from bs4 import BeautifulSoup
from datetime import datetime
import math

from JJE_App.settings import LEAGUE_ID, STARTING_WEEK


def create_session():
    token = UserToken.objects.get(standings_token=True)
    token = refresh_user_token(token)
    oauth = create_oauth_session(_client_id=token.client_id,
                                 token=token.access_token)
    return oauth


def update_standings():
    yahoo_obj = create_session()
    set_standings_not_current()
    get_new_standings(yahoo_obj)


def set_standings_not_current():
    for item in YahooStanding.objects.all():
        item.current_standings = False
        item.save()


def get_new_standings(yahoo_obj):
    url = "https://fantasysports.yahooapis.com/" \
          "fantasy/v2/league/{}/standings".format(LEAGUE_ID)

    result = yahoo_obj.request("get", url)
    results, status_code = result.text, result.status_code
    if (result.text is None) or (result.status_code != 200):
        # 'Means an error with the yahoo stuff'
        print("Error with yahoo")
        return False

    standings_soup = BeautifulSoup(result.text, 'html.parser')
    team_list = league_standings(standings_soup)

    return True


def league_standings(xml_data=None):
    """
    Pass the xmlData in AS a beautiful soup object
    team_list is a series of model objects that can be saved on return
    """
    team_list = []
    teams = xml_data.findAll('team')
    for team in teams:
        team_id, team_name, guid_objects = _process_team_row(team)

        standings_class = _process_standings(
            team, team_name, guid_objects
        )

        # team_list.append(
        #     {
        #         'team': team_class,
        #         'standings': standings_class,
        #         'new_team': new_team}
        # )
    return team_list


def _process_team_to_dct(teams):
    guid_dct = {}
    for team in teams:

        team_id = team.find('team_id').text
        team_name = team.find('name').text
        logo_url = team.find('team_logo').find('url').text
        manager = team.find('manager')
        manager_name = manager.find('nickname').text
        manager_email = manager.find('email').text
        manager_guid = manager.find('guid').text

        x = guid_dct.get(manager_guid, [])
        x.append({
            'team_id': team_id,
            'team_name': team_name,
            'logo_url': logo_url,
            'manager': manager,
            'manager_name': manager_name,
            'manager_email': manager_email
        })
        guid_dct[manager_guid] = x
    return guid_dct


def _process_team_row(team_row_xml):
    team_id = team_row_xml.find('team_id').text
    team_name = team_row_xml.find('name').text
    guids = _get_managers(team_row_xml)
    return team_id, team_name, guids


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


def _process_standings(team_row_xml, team_name, guid_objects):
    standings_class = YahooStanding()

    standings_class.team_name = team_name
    # standings_class.yahoo_guid = guid_objects

    standings_class.rank = _process_rank(team_row_xml)

    standings_class = _process_team_stats(standings_class, team_row_xml)
    standings_class = _process_team_points(standings_class, team_row_xml)

    starting_week = STARTING_WEEK

    standings_class.standings_week = math.floor(
        ((datetime.utcnow() - starting_week).days / 7)
    )

    standings_class.current_standings = True
    standings_class.save()

    for guid_obj in guid_objects:
        standings_class.yahoo_guid.add(guid_obj)
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
