from django.utils import timezone
from rest_framework import exceptions, mixins, viewsets

from alerts import serializers, models


class AlertViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):
    '''Alerts allow for create, update, retrieve and list (but not destroy)'''

    get_queryset = models.Alert.objects.all
    serializer_class = serializers.AlertSerializer
    filter_fields = ('username', 'text')

    def filter_queryset(self, queryset):
        active = self.request.query_params.get('active')
        if active:
            if int(active):
                queryset = queryset.active()
            else:
                queryset = quertyset.inactive()
        cleared = self.request.query_params.get('cleared')
        if cleared:
            if int(cleared):
                queryset = queryset.cleared()
            else:
                queryset = quertyset.uncleared()
        pending = self.request.query_params.get('pending')
        if pending:
            if int(pending):
                queryset = queryset.pending()
            else:
                queryset = quertyset.not_pending()
        return super(AlertViewSet, self).filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        requests.data['set_on'] = requests.data['cleared_on'] = None
        super(AlertViewSet.self).create(request, *args, **kwargs)

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
        super(AlertViewSet.self).update(request, *args, **kwargs)
