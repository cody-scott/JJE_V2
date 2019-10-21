from django.core.management.base import BaseCommand, CommandError
from JJE_Standings.utils.yahoo_data import update_standings


class Command(BaseCommand):
    help = 'Update current standings'

    def handle(self, *args, **options):
        update_standings()
