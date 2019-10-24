from JJE_Main.models import YahooTeam, YahooGUID
from allauth.account.models import EmailAddress
from django.conf import settings


def get_users_teams_waivers(guid):
    team_list = []
    for t in get_users_teams_qs(guid):
        team_list.append({'id': t.id, 'team_id': t.team_id, 'team_name': t.team_name})

    return team_list


def get_users_teams_ids(guid):
    team_list = [t.id for t in get_users_teams_qs(guid)]
    return team_list


def get_users_teams_qs(guid):
    guid_objs = YahooGUID.objects.filter(yahoo_guid=guid) # type: YahooGUID
    if len(guid_objs) == 0:
        return []

    team_list = []
    guid_obj = guid_objs[0]
    return guid_obj.yahoo_team.all()


def get_teams_qs(team_list):
    team_objs = YahooTeam.objects.filter(id__in=team_list)
    return team_objs


def get_emails():
    if settings.EMAIL_LEVEL == 'SUPER_USER':
        emails = EmailAddress.objects.filter(user__is_superuser=True)
    elif settings.EMAIL_LEVEL == 'STAFF':
        emails = EmailAddress.objects.filter(user__is_staff=True)
    else:
        emails = EmailAddress.objects.all()
    e = [val.email for val in emails.filter(verified=True)]
    return e
