from rest_framework import serializers
from JJE_Main.models import YahooGUID, YahooTeam
from allauth.account.models import EmailAddress


class YahooTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = YahooTeam
        fields = (
            'id',
            'team_id',
            'team_name',
            'logo_url',
        )


class YahooCurrentGUIDSerializer(serializers.ModelSerializer):
    yahoo_team = YahooTeamSerializer(many=True)

    class Meta:
        model = YahooGUID

        fields = (
            'manager_name',
            'yahoo_guid',
            'yahoo_team',
        )


class YahooTeamOnlySerializer(serializers.ModelSerializer):
    yahoo_team = YahooTeamSerializer(many=True)

    class Meta:
        model = YahooGUID

        fields = (
            'yahoo_team',
        )
