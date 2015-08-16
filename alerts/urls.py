from alerts import api
from server.router import router

router.register(
    'alerts', api.AlertViewSet, base_name='alert')
