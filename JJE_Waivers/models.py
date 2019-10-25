from django.db import models
from django.utils import timezone
from django.urls import reverse
import datetime

from JJE_Main.models import YahooTeam


class WaiverClaim(models.Model):
    # yahoo_team_uid = models.IntegerField()
    yahoo_team = models.ForeignKey(YahooTeam, default=None, blank=True, null=True, on_delete=models.SET_NULL,
                      related_name='waiver_team')

    claim_start = models.DateTimeField(default=timezone.now)

    add_player = models.CharField(max_length=255)

    add_LW = models.BooleanField(default=False)
    add_C = models.BooleanField(default=False)
    add_RW = models.BooleanField(default=False)
    add_D = models.BooleanField(default=False)
    add_G = models.BooleanField(default=False)
    add_Util = models.BooleanField(default=False)
    add_IR = models.BooleanField(default=False)

    drop_player = models.CharField(max_length=255)

    drop_LW = models.BooleanField(default=False)
    drop_C = models.BooleanField(default=False)
    drop_RW = models.BooleanField(default=False)
    drop_D = models.BooleanField(default=False)
    drop_G = models.BooleanField(default=False)
    drop_Util = models.BooleanField(default=False)
    drop_IR = models.BooleanField(default=False)

    over_claim_id = models.IntegerField(default=0)

    overclaimed = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    claim_message = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('index')
        # return reverse('waiver-claim-detail', kwargs={'pk': self.pk})

    def active_claim(self):
        time_difference = self.claim_start + datetime.timedelta(days=1)
        if (not self.overclaimed)\
                and (not self.cancelled)\
                and time_difference >= timezone.now():
            return True
        else:
            return False

    active_claim.admin_order_field = 'claim_start'
    active_claim.boolean = True
    active_claim.short_description = "Is Active"

    def get_position_string(self):
        out_positions_add = self.get_position_add
        out_positions_drop = self.get_position_drop

        return out_positions_add, out_positions_drop

    @property
    def get_position_add(self):
        add = {
            "LW": self.add_LW, "C": self.add_C, "RW": self.add_RW,
            "D": self.add_D, "G": self.add_G,
            "Utils": self.add_Util, "IR": self.add_IR
        }
        out_positions_add = "/".join(
            [item
             for item in add if add[item] is True
             ]
        )
        return out_positions_add

    @property
    def get_position_drop(self):
        drop = {
            "LW": self.drop_LW, "C": self.drop_C, "RW": self.drop_RW,
            "D": self.drop_D, "G": self.drop_G,
            "Utils": self.drop_Util, "IR": self.drop_IR
        }
        out_positions_drop = "/".join([
            item
            for item in drop
            if drop[item] is True]
        )
        return out_positions_drop

    @property
    def claim_end_iso(self):
        return self.claim_end_normal.isoformat()

    @property
    def claim_end_normal(self):
        return self.claim_start + datetime.timedelta(days=1)

    def __str__(self):
        return self.add_player

    class Meta:
        ordering = ['-claim_start']
