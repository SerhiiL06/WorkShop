from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()

router.register(r"orders", views.OrderViewSet)
router.register(r"master-order", views.MasterOrderViewSet)


urlpatterns = []


urlpatterns += router.urls
