
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from finance.views.subscription_view import SubscriptionViewSet

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = router.urls
