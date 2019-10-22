from django.core.mail import send_mail
from django.template import Context, Template

from JJE_Waivers.models import YahooTeam, WaiverClaim

from JJE_App.settings import email_super_users, email_admins, send_emails
from django.contrib.auth.models import User

from allauth.account.models import EmailAddress

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


def claim_email(waiver_claim, claim_type, request):
    send_waiver_email(waiver_claim, claim_type, request)


def cancel_email(waiver_claim, request):
    body = render_to_string("JJE_Waivers/cancel_claim.html",
                            {
                                "claim": waiver_claim,
                                "site": get_current_site(request),
                            })
    body_non_html = "{}]n{}".format(
        waiver_claim.team.team_name,
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
        waiver_object.team.team_name,
        waiver_object.add_player,
        waiver_object.drop_player,
        waiver_object.claim_start,
        waiver_object.claim_end_normal
    )

    subject = "John Jones - {}".format(message_type)
    return subject, body, body_non_html


def construct_send_email(subject, body_non_html, body):
    if email_super_users:
        emails = superuser_emails()
    elif email_admins:
        emails = admin_emails()
    else:
        emails = get_available_emails()

    if send_emails:
        send_mail(
            subject=subject,
            message=body_non_html,
            from_email="jje.waivers@gmail.com",
            html_message=body, recipient_list=emails
        )


def get_available_emails():
    return [
        email.email
        for email in EmailAddress.objects.all()
        if email.verified
    ]


def superuser_emails():
    emails = []
    for email in EmailAddress.objects.all():
        if not email.verified:
            continue
        if email.user.is_superuser:
            emails.append(email.email)
    return emails


def admin_emails():
    emails = []
    for email in EmailAddress.objects.all():
        if not email.verified:
            continue
        if email.user.is_staff:
            emails.append(email.email)
    return emails
