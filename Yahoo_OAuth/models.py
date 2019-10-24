from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import datetime


class UserToken(models.Model):
    """This is just for the API to collect and update the app"""
    date_created = models.DateTimeField(auto_now=True)
    client_id = models.TextField()
    client_secret = models.TextField()
    access_token = models.TextField()
    refresh_token = models.TextField()
    user_guid = models.TextField()

    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.SET_NULL)

    def __repr__(self):
        return "<ID: {}>".format(self.id)

    @property
    def expired(self):
        now = timezone.now()
        expiry_time = (self.date_created + datetime.timedelta(hours=1))
        if expiry_time > now:
            return False
        else:
            return True
