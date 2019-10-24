from django.core.management.base import BaseCommand, CommandError

from django.contrib.sites.models import Site
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Setup Site'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        s = Site.objects.first()
        s.domain = "https://www.myapp.test/"
        s.name = "Development URL"
        s.save()

        for u in User.objects.all():
            u.is_staff = True
            u.is_superuser = True
            u.save()