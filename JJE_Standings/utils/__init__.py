from JJE_Standings.models import YahooStanding
from JJE_Waivers.models import YahooTeam

from JJE_Standings.utils.standing_emails import send_standings_email
from django.utils import timezone

import json


def email_standings():
    standings = get_standings()
    send_standings_email(standings)


def get_standings():
    # try:
        out_teams = []
        standings = YahooStanding.objects.filter(current_standings=True)
        for standing in standings:
            # i think the -1 will get the most recent
            # if there is any team that is missed,
            # then this will be screwed up so run again
            out_teams.append([standing.team.team_id,
                              standing.team.team_name,
                              standing.rank,
                              standing.stat_point_total,
                              standing.team.logo_url])

        # sorts the list based on the rank (index 2)
        yahoo_standings_list = sorted(out_teams, key=lambda x: x[2])

        return yahoo_standings_list


def get_standings_json(guid=None):
    newstandings = get_standings()
    tmls = []
    if guid is not None:
        tm = YahooTeam.objects.filter_by(manager_guid=guid).all()
        for team in tm:
            tmls.append(team.team_id)

    od = []
    for item in newstandings:
        team_flag = 0
        if item[0] in tmls:
            team_flag = 1

        od.append({
            "TeamID": item[0],
            "TeamName": item[1],
            "TeamRank": item[2],
            "TeamPoints": item[3],
            "TeamURL": item[4],
            # "UserTeam": team_flag,
        })

    return json.dumps(od, indent=4)


def check_if_update_required():
    try:
        standings = YahooStanding.objects.filter(
            current_standings=True
        ).first()

        now = timezone.now()
        diff = (now - standings.date_created)

        if diff.days > 6:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return True
