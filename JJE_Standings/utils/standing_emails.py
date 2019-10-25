from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from JJE_Main.utils import jje_main_functions

from JJE_Standings.models import YahooStanding


def send_standings_email():
    standings = YahooStanding.objects.filter(current_standings=True).order_by('rank')

    standings_non_html = "\n".join(
        ["\t".join(
            [str(item.rank), str(item.yahoo_team.team_name), str(item.stat_point_total)])
            for item in standings]
    )
    standings_html = render_to_string(
        "JJE_Standings/email_template.html",
        {"DATA": standings, "DATETIME": timezone.now()})

    subject = "JJE Standings - Week {}".format(standings[0].standings_week)
    construct_send_email(subject, standings_non_html, standings_html)
    return standings_html


def construct_send_email(subject, body_non_html, body):
    emails = jje_main_functions.get_emails()

    if settings.SEND_EMAIL is True:
        send_mail(
            subject=subject,
            message=body_non_html,
            from_email="jje.waivers@gmail.com",
            html_message=body, recipient_list=emails
        )
