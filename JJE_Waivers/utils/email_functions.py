from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import send_mail

from django.conf import settings
from JJE_Main.utils import jje_main_functions


def claim_email(waiver_claim, claim_type, request):
    send_waiver_email(waiver_claim, claim_type, request)


def cancel_email(waiver_claim, request):
    body = render_to_string("JJE_Waivers/cancel_claim.html",
                            {
                                "claim": waiver_claim,
                                "site": get_current_site(request),
                            })
    body_non_html = "{}\n{}".format(
        waiver_claim.yahoo_team.team_name,
        waiver_claim.add_player
    )
    construct_send_email("Cancelled Claim", body_non_html, body)


def send_waiver_email(waiver_object, message_type, request):
    subject, body, body_non_html = format_waiver_claim(
        waiver_object, message_type, request)
    construct_send_email(
        subject=subject, body=body, body_non_html=body_non_html)


def format_waiver_claim(waiver_object, message_type, request):
    waiver_object = waiver_object #type: WaiverClaim

    move_to_ir = waiver_object.drop_IR

    body = render_to_string("JJE_Waivers/email_claim.html", {
        "claim": waiver_object,
        "site": get_current_site(request),
        "IR_PLAYER": move_to_ir
    })

    body_non_html = "{}\n{}\n{}\n{}\n{}".format(
        waiver_object.yahoo_team.team_name,
        waiver_object.add_player,
        waiver_object.drop_player,
        waiver_object.claim_start,
        waiver_object.claim_end_normal
    )

    subject = "John Jones - {}".format(message_type)
    return subject, body, body_non_html


def construct_send_email(subject, body_non_html, body):
    emails = jje_main_functions.get_emails()

    if settings.SEND_EMAIL is True:
        send_mail(
            subject=subject,
            message=body_non_html,
            from_email="jje.waivers@gmail.com",
            html_message=body, recipient_list=emails
        )
