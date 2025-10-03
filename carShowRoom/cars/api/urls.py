from rest_framework.routers import DefaultRouter
from .views import CarsViewSet

router = DefaultRouter()
router.register(r'cars', CarsViewSet)

urlpatterns = router.urls
