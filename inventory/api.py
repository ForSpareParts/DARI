from django.utils import timezone
from rest_framework import exceptions, mixins, viewsets

from inventory import serializers, models


class ItemViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):

    get_queryset = models.Item.objects.all
    serializer_class = serializers.ItemSerializer
    filter_fields = ('location', 'category', 'name', 'material_number',
        'serial_number', 'date_received', 'kit', 'notes', 'sort_by_name',
        'manual', 'qty_at_inventory', 'inventory_loaded_on',
        'last_modified_on', 'current_qty', 'superceded_by')

    def filter_queryset(self, queryset):
        superceded = self.request.query_params.get('superceded')
        if superceded:
            if int(superceded):
                queryset = queryset.exclude(superceded_by=None)
            else:
                queryset = queryset.filter(superceded_by=None)
        return super(ItemViewSet, self).filter_queryset(queryset)


class ItemRequisitionViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):

    get_queryset = models.ItemRequisition.objects.all
    serializer_class = serializers.ItemRequisitionSerializer
    filter_fields = ('item', 'checked_out_by', 'checked_out_on',
        'checked_in_on', 'last_modified_on')

    def filter_queryset(self, queryset):
        closed = self.request.query_params.get('closed')
        if closed:
            if int(closed):
                queryset = queryset.exclude(checked_on_on=None)
            else:
                queryset = queryset.filter(checked_on_on=None)
        return super(ItemRequisitionViewSet, self).filter_queryset(queryset)
