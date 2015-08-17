from rest_framework import serializers

from alerts import models


class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Alert
