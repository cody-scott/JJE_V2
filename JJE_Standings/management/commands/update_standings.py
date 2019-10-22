from django.core.management.base import BaseCommand, CommandError
from JJE_Standings.utils.yahoo_data import update_standings


class Command(BaseCommand):
    help = 'Update current standings'

    def add_arguments(self, parser):
        parser.add_argument('token')

    def handle(self, *args, **options):
        token = options.get('token')
        if token is None:
            print("Error")
        update_standings(token)
