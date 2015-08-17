from inventory import api
from server.router import router

router.register(
    'items', api.ItemViewSet, base_name='item')

router.register(
    'item-requisitions', api.ItemRequisitionViewSet,
    base_name='itemrequisition')
