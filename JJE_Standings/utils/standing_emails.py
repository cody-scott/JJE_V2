from django.template.loader import render_to_string
from django.utils import timezone

from JJE_Standings.models import YahooStanding

from JJE_Waivers.utils.email_functions import construct_send_email


def send_standings_email(standings_html):
    standings_non_html = "\n".join(
        ["\t".join(
            [str(item[2]), str(item[1]), str(item[3])])
            for item in standings_html]
    )
    standings_html = render_to_string(
        "JJE_Standings/email_template.html",
        {"DATA": standings_html, "DATETIME": timezone.now()})
    week = YahooStanding.objects.filter(
        current_standings=True).first().standings_week

    subject = "JJE Standings - Week {}".format(week)
    construct_send_email(subject, standings_non_html, standings_html)
    return standings_html
