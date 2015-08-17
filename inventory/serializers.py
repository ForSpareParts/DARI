from rest_framework import serializers

from inventory import models


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Item


class ItemRequisitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ItemRequisition
