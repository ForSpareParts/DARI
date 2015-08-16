from django.db import models
from django.utils import timezone

# Create your models here.


class AlertQuerySet(models.QuerySet):

    def active(self):
        return self.filter(alert_on__lte=timezone.now(), cleared_on=None)

    def inactive(self):
        return self.exclude(alert_on__lte=timezone.now(), cleared_on=None)

    def cleared(self):
        return self.exclude(cleared_on=None)

    def uncleared(self):
        return self.filter(cleared_on=None)

    def pending(self):
        return self.filter(alert_on__gt=timezone.now(), cleared_on=None)

    def not_pending(self):
        return self.exclude(alert_on__gt=timezone.now(), cleared_on=None)


class Alert(models.Model):

    username = models.CharField(max_length=255)
    text = models.TextField(blank=True, default='')
    set_on = models.DateTimeField(auto_now_add=True)
    alert_on = models.DateTimeField(blank=True, default=timezone.now) 
    cleared_on = models.DateTimeField(blank=True, null=True)

    objects = AlertQuerySet.as_manager()
