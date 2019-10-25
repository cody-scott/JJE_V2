from django.core.management.base import BaseCommand, CommandError
from JJE_Standings.utils.yahoo_data import update_standings
from JJE_Standings.utils import standing_emails

from django.contrib.sites.models import Site
from django.conf import settings

import requests


class Command(BaseCommand):
    help = 'Update current standings'

    def add_arguments(self, parser):
        parser.add_argument('token')

    def handle(self, *args, **options):
        token = options.get('token')
        if token is None:
            print("Error")

        # this is to wake up the website if not running
        site = Site.objects.first()
        requests.get(site.domain, verify=settings.VERIFY_REQUEST)

        if update_standings(token) is True:
            standing_emails.send_standings_email()
