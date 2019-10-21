from JJE_Standings.models import YahooStanding

from Yahoo_Authentication.utils.oauth_flow import refresh_user_token, create_oauth_session
from Yahoo_Authentication.models import UserToken

from bs4 import BeautifulSoup
from datetime import datetime
import math

from JJE_App.settings import LEAGUE_ID


def create_session(request):
    token = UserToken.objects.get(standings_token=True)
    oauth = create_oauth_session(_client_id=token.client_id,
                                 token=token.access_token)

    refresh_user_token(request, token)
    token = UserToken.objects.get(standings_token=True)
    oauth = create_oauth_session(_client_id=token.client_id,
                                 token=token.access_token)
    return oauth


def build_team_data(request):
    yahoo_obj = create_session(request)
    url = "https://fantasysports.yahooapis.com/" \
          "fantasy/v2/league/{}/standings".format(LEAGUE_ID)

    result = yahoo_obj.get(url)
    results, status_code = result.text, result.status_code
    if (result.text is None) or (result.status_code != 200):
        'Means an error with the yahoo stuff'
        return False

    standings_soup = BeautifulSoup(result.text, 'html.parser')
    teams = standings_soup.findAll('team')
    for team in teams:
        _process_team(team)
    return True


def test_standings(request):
    yahoo_obj = create_session(request)
    url = "https://fantasysports.yahooapis.com/" \
          "fantasy/v2/league/{}/standings".format(LEAGUE_ID)

    result = yahoo_obj.request("get", url)
    results, status_code = result.text, result.status_code

    return result, status_code


def update_standings(request):
    yahoo_obj = create_session(request)
    set_standings_not_current()
    _standings_collection(yahoo_obj)


def set_standings_not_current():
    for item in YahooStanding.objects.all():
        item.current_standings = False
        item.save()


def _standings_collection(yahoo_obj):
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
        team_class, new_team = _process_team(team)

        standings_class = _process_standings(
            team_class, team, team_class.team_id
        )

        team_list.append(
            {
                'team': team_class,
                'standings': standings_class,
                'new_team': new_team}
        )
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



def _process_team(team_row_xml):
    new_team = False
    # get the team id
    team_id = team_row_xml.find('team_id').text
    # Check if exists in the db
    team_class = YahooTeam.objects.filter(team_id=team_id).first()

    # If it doesn't exist then make a new one -> won't return None if it exist
    if team_class is None:
        new_team = True
        team_class = YahooTeam()

    team_class.team_id = team_row_xml.find('team_id').text
    team_class.team_name = team_row_xml.find('name').text
    team_class.logo_url = team_row_xml.find('team_logo').find('url').text

    manager = team_row_xml.find('manager')
    team_class.manager_name = manager.find('nickname').text
    team_class.manager_email = manager.find('email').text
    team_class.manager_guid = manager.find('guid').text

    team_class.save()

    return [team_class, new_team]


def _process_standings(team_class, team_row_xml, team_id):
    standings_class = YahooStanding()

    standings_class.team = team_class

    standings_class.rank = _process_rank(team_row_xml)

    standings_class = _process_team_stats(standings_class, team_row_xml)
    standings_class = _process_team_points(standings_class, team_row_xml)

    starting_week = datetime.strptime(
        "2018-10-03 00:00:00.000000", "%Y-%m-%d %H:%M:%S.%f"
    )
    standings_class.standings_week = math.floor(
        ((datetime.utcnow() - starting_week).days / 7)
    )

    standings_class.current_standings = True

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
