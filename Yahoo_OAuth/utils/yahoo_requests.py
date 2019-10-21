from Yahoo_OAuth.utils.oauth_flow import refresh_user_token, create_oauth_session
from Yahoo_OAuth.models import UserToken

from JJE_App.settings import LEAGUE_ID

from urllib.parse import urlencode


def create_session(token):
    token = refresh_user_token(token)
    oauth = create_oauth_session(_client_id=token.client_id,
                                 token=token.access_token)
    return oauth


def get_standings():
    token = UserToken.objects.get(standings_token=True)
    yahoo_obj = create_session(token)
    request_standings(yahoo_obj)


def _get_request(yahoo_obj, url):
    result = yahoo_obj.request("get", url)
    results, status_code = result.text, result.status_code

    return {"results": result.text, "status_code": status_code}


def request_standings(yahoo_obj):
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/{LEAGUE_ID}/standings"
    return _get_request(yahoo_obj, url)


def request_roster(yahoo_obj, team_id):
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/team/{LEAGUE_ID}.t.{team_id}/roster/players"
    return _get_request(yahoo_obj, url)


def request_players(yahoo_obj, player_dict):
    player_args = urlencode(player_dict).replace("&", ",")
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/{LEAGUE_ID}/players;{player_args}/stats"
    return _get_request(yahoo_obj, url)


def request_player(yahoo_obj, player_id):
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/{LEAGUE_ID}/players;player_keys=nhl.p.{player_id}/stats"
    return _get_request(yahoo_obj, url)
