from rest_framework.routers import DefaultRouter  # автоматическая генерация URL для ViewSet

from .api_views import (
    ProductViewSet,
    CategoryViewSet,
    ManufacturerViewSet,
    CartItemViewSet,
)

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"manufacturers", ManufacturerViewSet)
router.register(r"cart-items", CartItemViewSet)

urlpatterns = router.urls
