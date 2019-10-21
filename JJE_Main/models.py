from django.db import models
from django.utils import timezone
from django.urls import reverse
import datetime
from django.contrib.auth.models import User


class YahooTeam(models.Model):
    team_id = models.CharField(max_length=10)
    team_name = models.CharField(max_length=50)
    logo_url = models.TextField(blank=True)
    manager_name = models.CharField(max_length=200, blank=True)
    manager_email = models.EmailField(blank=True)

    manager_guid = models.CharField(max_length=200, blank=True)

    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.team_name
