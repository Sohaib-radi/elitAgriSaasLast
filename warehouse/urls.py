

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from warehouse.views.content_type import WarehouseContentTypeListView
from warehouse.views.warehouse import WarehouseViewSet, WarehouseImageViewSet, WarehouseVideoViewSet
from warehouse.views.entry import WarehouseEntryViewSet
from warehouse.views.quantity_control import WarehouseReminderViewSet
from warehouse.views.quantity_control import WarehouseQuantityScheduleViewSet
from warehouse.views.warehouse import WarehouseViewSet
from warehouse.views.statistics import WarehouseStatisticsView
router = DefaultRouter()
router.register("warehouses", WarehouseViewSet, basename="warehouses")
router.register("warehouse-images", WarehouseImageViewSet, basename="warehouse-images")
router.register("warehouse-videos", WarehouseVideoViewSet, basename="warehouse-videos")
router.register("entries", WarehouseEntryViewSet, basename="warehouse-entries")
router.register("quantity-schedules", WarehouseQuantityScheduleViewSet, basename="warehouse-schedules")
router.register("reminders", WarehouseReminderViewSet, basename="warehouse-reminders")

urlpatterns = [
    path("", include(router.urls)),
    path("content-types/", WarehouseContentTypeListView.as_view(), name="warehouse-content-types"),
    path("<int:pk>/statistics/", WarehouseStatisticsView.as_view(), name="warehouse-statistics"),
]
