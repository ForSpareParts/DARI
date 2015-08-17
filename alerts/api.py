from django.utils import timezone
from rest_framework import exceptions, mixins, viewsets

from alerts import serializers, models


class AlertViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):

    get_queryset = models.Alert.objects.all
    serializer_class = serializers.AlertSerializer
    filter_fields = ('username', 'type', 'text')

    def filter_queryset(self, queryset):
        active = self.request.query_params.get('active')
        if active:
            if int(active):
                queryset = queryset.active()
            else:
                queryset = queryset.inactive()
        cleared = self.request.query_params.get('cleared')
        if cleared:
            if int(cleared):
                queryset = queryset.cleared()
            else:
                queryset = queryset.uncleared()
        pending = self.request.query_params.get('pending')
        if pending:
            if int(pending):
                queryset = queryset.pending()
            else:
                queryset = queryset.not_pending()
        return super(AlertViewSet, self).filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        request.data['set_on'] = request.data['cleared_on'] = None
        return super(AlertViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        for key in request.data.keys():
            if key == 'cleared':
                clear = int(request['cleared'])
                if clear:
                    request['cleared_on'] = timezone.now()
                else:
                    request['cleared_on'] = None
            else:
                raise exceptions.ValidationError('You may only clear and '
                    'unclear existing alerts')
        return super(AlertViewSet, self).update(request, *args, **kwargs)
