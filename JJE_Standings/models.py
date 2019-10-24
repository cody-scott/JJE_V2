from django.db import models

from JJE_Main.models import YahooTeam as _YahooTeam


class YahooStanding(models.Model):
    """Weekly standings from Yahoo"""
    date_created = models.DateTimeField(auto_now=True)

    # yahoo_team_uid = models.IntegerField()
    yahoo_team = models.ForeignKey(_YahooTeam, default=None, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='standing_team')

    rank = models.IntegerField()
    stat_point_total = models.FloatField()

    stat_1 = models.FloatField()
    stat_2 = models.FloatField()
    stat_3 = models.FloatField()
    stat_4 = models.FloatField()
    stat_5 = models.FloatField()
    stat_8 = models.FloatField()
    stat_12 = models.FloatField()
    stat_31 = models.FloatField()
    stat_19 = models.FloatField()
    stat_22 = models.FloatField()
    stat_23 = models.FloatField()
    stat_25 = models.FloatField()
    stat_24 = models.FloatField()
    stat_26 = models.FloatField()
    stat_27 = models.FloatField()

    stat_points_1 = models.FloatField()
    stat_points_2 = models.FloatField()
    stat_points_3 = models.FloatField()
    stat_points_4 = models.FloatField()
    stat_points_5 = models.FloatField()
    stat_points_8 = models.FloatField()
    stat_points_12 = models.FloatField()
    stat_points_31 = models.FloatField()
    stat_points_19 = models.FloatField()
    stat_points_22 = models.FloatField()
    stat_points_23 = models.FloatField()
    stat_points_25 = models.FloatField()
    stat_points_24 = models.FloatField()
    stat_points_26 = models.FloatField()
    stat_points_27 = models.FloatField()

    standings_week = models.IntegerField()

    current_standings = models.BooleanField(default=False)

    def __str__(self):
        return "<id: {}>".format(self.yahoo_team.team_name)

    class Meta:
        ordering = ['current_standings', 'rank']
        verbose_name = 'Yahoo Standing'
        verbose_name_plural = 'Yahoo Standings'


class StandingsRequestHistory(models.Model):
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']


