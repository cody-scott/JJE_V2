from django.core.management.base import BaseCommand, CommandError

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

class Command(BaseCommand):
    help = 'Setup Site'

    def add_arguments(self, parser):
        parser.add_argument('domain')
        parser.add_argument('name')

    def handle(self, *args, **options):
        s = Site.objects.first()
        s.domain = options.get('domain')
        s.name = options.get('name')
        s.save()

        for u in User.objects.all():
            u.is_staff = True
            u.is_superuser = True
            u.save()

        for v in EmailAddress.objects.all():
            v.verified = True
            v.save()
