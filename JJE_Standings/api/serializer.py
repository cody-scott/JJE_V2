from rest_framework import serializers
from JJE_Standings.models import YahooStanding
from JJE_Main.models import YahooTeam


class YahooStandingsAllStandingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = YahooStanding
        fields = (
            'standings_week',
            'rank',
            'stat_point_total',
        )


class YahooTeamAllStandingsSerializer(serializers.ModelSerializer):
    standing_team = YahooStandingsAllStandingsSerializer(many=True)
    class Meta:
        model = YahooTeam
        fields = (
            'team_id',
            'team_name',
            'standing_team',
        )


class YahooRankSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='yahoo_team.id')
    team_id = serializers.CharField(source='yahoo_team.team_id')
    team_name = serializers.CharField(source='yahoo_team.team_name')
    logo_url = serializers.URLField(source='yahoo_team.logo_url')
    current_rank = serializers.IntegerField(source='rank')

    class Meta:
        model = YahooStanding
        fields = (
            'id', 'team_id', 'team_name', 'current_rank', 'stat_point_total', 'standings_week', 'logo_url',
        )
