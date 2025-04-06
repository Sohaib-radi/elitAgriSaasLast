from rest_framework.routers import DefaultRouter
from product_catalogue.views.product import ProductViewSet, ProductCategoryViewSet, ProductVariantViewSet
from product_catalogue.views.supplier import SupplierListViewSet, SupplierViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', ProductCategoryViewSet, basename='product-category')
router.register(r'variants', ProductVariantViewSet, basename='product-variant')
router.register(r'supplier-lists', SupplierListViewSet, basename="supplier-list")
router.register(r'suppliers', SupplierViewSet, basename="supplier")
urlpatterns = router.urls