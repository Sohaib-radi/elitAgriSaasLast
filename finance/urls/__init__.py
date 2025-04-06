from django.urls import path, include

urlpatterns = [
    path("expenses/", include("finance.urls.expense_urls")),
    path("vouchers/", include("finance.urls.payment_urls")),
]