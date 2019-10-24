from JJE_Standings.models import YahooStanding


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