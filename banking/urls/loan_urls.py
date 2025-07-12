from django.urls import path, include
from rest_framework.routers import DefaultRouter
from banking.views.loan_view import LoanViewSet

router = DefaultRouter()
router.register(r"loans", LoanViewSet, basename="loan")

urlpatterns = [
    path("", include(router.urls)),
]