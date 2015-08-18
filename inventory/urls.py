from django.conf.urls import include, url

from inventory import api, views
from server.router import router

router.register(
    'items', api.ItemViewSet, base_name='item')

router.register(
    'item-requisitions', api.ItemRequisitionViewSet,
    base_name='itemrequisition')


urlpatterns = [
    url(r'^checkout/', views.CheckOutView.as_view(), name='checkout'),
    url(r'^checkin/', views.CheckInView.as_view(), name='checkin'),
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
]
