from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions

from rest_framework.decorators import api_view, permission_classes

from Yahoo_OAuth.utils import yahoo_requests


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_standings(request):
    return Response(yahoo_requests.get_standings(request))


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_team(request):
    return Response(yahoo_requests.get_user_teams(request))


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_teams(request):
    return Response(yahoo_requests.get_teams(request))
