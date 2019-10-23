from django.db import models
from django.utils import timezone
from django.urls import reverse
import datetime
from django.contrib.auth.models import User


class YahooTeam(models.Model):
    team_id = models.CharField(max_length=10)
    team_name = models.CharField(max_length=50)
    logo_url = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.team_name

    class Meta:
        verbose_name = 'Yahoo Team'
        verbose_name_plural = 'Yahoo Teams'


class YahooGUID(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    yahoo_guid = models.CharField(max_length=150)
    manager_name = models.CharField(max_length=150)

    yahoo_team = models.ManyToManyField(YahooTeam, related_name='guid_teams')

    def __str__(self):
        return "<id: {}>".format(self.manager_name)

    class Meta:
        verbose_name = 'Yahoo GUID'
        verbose_name_plural = 'Yahoo GUIDs'
