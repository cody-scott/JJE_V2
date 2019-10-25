from JJE_Standings.models import YahooStanding


def get_overclaim_teams(team_list):
    team_standings = YahooStanding.objects.filter(current_standings=True).filter(yahoo_team_id__in=team_list)
    if len(team_standings) == 0:
        return []
    max_rank = max([t.rank for t in team_standings])
    overclaim_teams = YahooStanding.objects.filter(current_standings=True).filter(rank__lt=max_rank)
    overclaim_ids = [t.yahoo_team.id for t in overclaim_teams]
    return overclaim_ids


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


def get_rank_of_team(team_id):
    teams = YahooStanding.objects.filter(current_standings=True).filter(yahoo_team_id=team_id)
    if len(teams) == [0]:
        return 99
    return teams[0].rank