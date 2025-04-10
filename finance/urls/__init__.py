from django.urls import path, include

urlpatterns = [
    path("expenses/", include("finance.urls.expense_urls")),
    path("vouchers/", include("finance.urls.payment_urls")),
    path("", include("finance.urls.subscription_urls")),
    path("debts/", include("finance.urls.debt_urls")), 
    path("sales/", include("finance.urls.sales_invoice_urls")),
    path("purchases/", include("finance.urls.purchase_urls")),

]