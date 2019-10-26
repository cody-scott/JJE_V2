from Yahoo_OAuth.utils.oauth_flow import refresh_user_token, create_oauth_session
from Yahoo_OAuth.models import UserToken

from django.conf import settings
from urllib.parse import urlencode


from JJE_App.settings import BASE_DIR
import os


def _get_local(file_name):
    # todo remove this
    with open(os.path.join(BASE_DIR, f'test_files/{file_name}'), 'r') as fl:
        return {'results': fl.read(), 'status_code': 200}


def create_session(token):
    token = refresh_user_token(token)
    oauth = create_oauth_session(_client_id=token.client_id,
                                 token=token.access_token)
    return oauth


def get_standings(request):
    # return _get_local('standings.txt')

    token = request.user.usertoken_set.first()
    # token = UserToken.objects.get(standings_token=True)
    yahoo_obj = create_session(token)
    return request_standings(yahoo_obj)


def get_teams(request):
    # return _get_local('standings.txt')

    token = request.user.usertoken_set.first()
    yahoo_obj = create_session(token)
    r = request_teams(yahoo_obj)
    return r


def get_user_teams(request):
    # return _get_local('userteams.txt')

    token = request.user.usertoken_set.first()
    yahoo_obj = create_session(token)
    r = request_teams(yahoo_obj, True)
    return r


def _get_request(yahoo_obj, url):
    result = yahoo_obj.request("get", url)
    results, status_code = result.text, result.status_code

    return {"results": result.text, "status_code": status_code}


def request_standings(yahoo_obj):
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/{settings.LEAGUE_ID}/standings"
    return _get_request(yahoo_obj, url)


def request_roster(yahoo_obj, team_id):
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/team/{settings.LEAGUE_ID}.t.{team_id}/roster/players"
    return _get_request(yahoo_obj, url)


def request_players(yahoo_obj, player_dict):
    player_args = urlencode(player_dict).replace("&", ",")
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/{settings.LEAGUE_ID}/players;{player_args}/stats"
    return _get_request(yahoo_obj, url)


def request_player(yahoo_obj, player_id):
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/{settings.LEAGUE_ID}/players;player_keys=nhl.p.{player_id}/stats"
    return _get_request(yahoo_obj, url)


def request_teams(yahoo_obj, use_login=False):
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/{settings.LEAGUE_ID}/teams"
    if use_login:
        url += ';use_login=1'

    return _get_request(yahoo_obj, url)
