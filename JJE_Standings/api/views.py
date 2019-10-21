# from rest_framework import viewsets
#
# from JJE_Standings.api import serializer
# from JJE_Standings.models import YahooStanding
#
#
# class StandingsViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = YahooStanding.objects.all()
#     serializer_class = serializer.YahooStandingSerializer
#
#
# class ActiveStandingsViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = YahooStanding.objects.all()
#     serializer_class = serializer.YahooStandingSerializer
#
#     def get_queryset(self):
#         standings_active = YahooStanding.objects.filter(
#             current_standings=True
#         )
#         return standings_active
