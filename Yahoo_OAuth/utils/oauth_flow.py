from django.contrib.sites.models import Site
from JJE_App.settings import client_id, client_secret
from requests_oauthlib import OAuth2Session
from django.shortcuts import redirect

from Yahoo_OAuth.models import UserToken

import os

auth_url = "https://api.login.yahoo.com/oauth2/request_auth"
token_url = "https://api.login.yahoo.com/oauth2/get_token"


def create_oauth_session(_client_id=None, state=None, token=None):
    c_i = client_id
    if _client_id is not None:
        c_i = _client_id
    redirect_uri = os.path.join(Site.objects.first().domain, r"oauth/callback")

    access_token = token
    if token is not None:
        access_token = {'access_token': token}

    oauth = OAuth2Session(c_i, redirect_uri=redirect_uri, state=state,
                          token=access_token)
    return oauth


def start_oauth(request):
    oauth = create_oauth_session()
    authorization_url, state = oauth.authorization_url(auth_url)

    request.session['oauth_state'] = ""
    request.session['oauth_state'] = state

    return redirect(authorization_url)


def callback_oauth(request):
    callback_url = Site.objects.first().domain + request.get_full_path()
    oauth = create_oauth_session(state=request.session['oauth_state'])
    token = oauth.fetch_token(token_url, client_secret=client_secret,
                              authorization_response=callback_url)
    save_new_token(token, request)


def save_new_token(token, request):
    access_token = token.get("access_token")
    refresh_token = token.get("refresh_token")
    guid = token.get("xoauth_yahoo_guid")

    user_token = UserToken()
    user_token.user = request.user

    user_token.client_id = client_id
    user_token.client_secret = client_secret
    user_token.access_token = access_token
    user_token.refresh_token = refresh_token
    user_token.user_guid = guid

    # if len(UserToken.objects.filter(standings_token=False)) == 0:
    #     user_token.standings_token = True

    user_token.save()

    return


def refresh_current_token(request):
    user = request.user
    user_token = user.usertokens_set.first()

    refresh_user_token(request, user_token)


def refresh_user_token(user_token):
    extra = {
        'client_id': user_token.client_id,
        'client_secret': user_token.client_secret,
    }

    oauth = create_oauth_session(_client_id=user_token.client_id)
    new_token = oauth.refresh_token(
        token_url,
        refresh_token=user_token.refresh_token,
        **extra
    )

    save_refresh_token(new_token, user_token)
    return user_token


def save_refresh_token(token, user_token=None):
    access_token = token.get("access_token")
    refresh_token = token.get("refresh_token")
    guid = token.get("xoauth_yahoo_guid")

    user_token.client_id = client_id
    user_token.client_secret = client_secret
    user_token.access_token = access_token
    user_token.refresh_token = refresh_token
    user_token.user_guid = guid

    user_token.save()

    return user_token
