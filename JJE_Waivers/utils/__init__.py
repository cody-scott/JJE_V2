
from JJE_Waivers.models import YahooTeam

from django.dispatch.dispatcher import receiver


def get_user_teams_list(user):
    out_dct = {}
    teams = YahooTeam.objects.filter(user=user.id)
    if len(teams) == 1:
        out_dct = {'team': teams[0].id}
    return out_dct


def get_current_ranks(user):

    """Gets all the teams that are not eligible for overclaim"""
    # If no current standings make overclaims off
    if len(YahooStanding.objects.all()) == 0:
        return [team.id for team in YahooTeam.objects.all()]

    ranks = []
    for item in user.yahooteam_set.all():
        ranks.extend(
            [
                z.rank
                for z in item.yahoostanding_set.filter(
                    current_standings=True).all()
            ]
        )

    rank = 0
    if len(ranks) > 0:
        rank = max(ranks)

    teams = [
        team.team.id
        for team in YahooStanding.objects.filter(
            current_standings=True, rank__gte=rank)
    ]
    return teams


def get_claim_rank(team):
    standings = [
        item.rank
        for item in team.yahoostanding_set.filter(
            current_standings=True).all()
    ]
    return standings


def show_oauth_link(request):
    """If both pass aka have a link, then dont show oauth link (AKA False)"""
    user = request.user
    if user.is_anonymous:
        return False

    if len(request.user.usertoken_set.all()) == 0:
        return True

    return False


def _check_user_token(user):
    if len(user.usertoken_set.all()) == 0:
        return False
    else:
        return True


def _check_user_team(user):
    if len(user.yahooteam_set.all()) == 0:
        return False
    else:
        return True


@receiver(oauth_complete_signal)
def assign_user_teams_from_token(request, **kwargs):
    user = request.user

    token = user.usertoken_set.first()

    teams = YahooTeam.objects.filter(manager_guid=token.user_guid).all()
    for team in teams:
        team.user = user
        team.save()

    return


def check_if_standings():
    """
    Returns true if there is standings that exist
    :return:
    :rtype:
    """
    if len(YahooStanding.objects.all()) == 0:
        return False
    else:
        return True
