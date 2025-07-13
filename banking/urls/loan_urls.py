from django.urls import path, include
from rest_framework.routers import DefaultRouter
from banking.views.loan_view import LoanDetailView, LoanViewSet

router = DefaultRouter()
router.register(r"loans", LoanViewSet, basename="loan")


urlpatterns = [
    path("", include(router.urls)),
path("loan/<int:pk>/detail/", LoanDetailView.as_view(), name="loan-detail"),

]