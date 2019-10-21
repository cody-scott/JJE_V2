from JJE_Standings.models import YahooStanding


def create_standing(team, rank=1):
    """
    adds standing record to the table
    :param team: team to have added
    :param rank: rank of the team
    :return:
    """
    standing = YahooStanding()
    standing.team = team
    standing.rank = rank
    standing.stat_point_total = 0

    standing.stat_1 = 0
    standing.stat_2 = 0
    standing.stat_3 = 0
    standing.stat_4 = 0
    standing.stat_5 = 0
    standing.stat_8 = 0
    standing.stat_12 = 0
    standing.stat_31 = 0
    standing.stat_19 = 0
    standing.stat_22 = 0
    standing.stat_23 = 0
    standing.stat_25 = 0
    standing.stat_24 = 0
    standing.stat_26 = 0
    standing.stat_27 = 0

    standing.stat_points_1 = 0
    standing.stat_points_2 = 0
    standing.stat_points_3 = 0
    standing.stat_points_4 = 0
    standing.stat_points_5 = 0
    standing.stat_points_8 = 0
    standing.stat_points_12 = 0
    standing.stat_points_31 = 0
    standing.stat_points_19 = 0
    standing.stat_points_22 = 0
    standing.stat_points_23 = 0
    standing.stat_points_25 = 0
    standing.stat_points_24 = 0
    standing.stat_points_26 = 0
    standing.stat_points_27 = 0
    standing.current_standings = True
    standing.standings_week = 1
    standing.save()
    return standing
