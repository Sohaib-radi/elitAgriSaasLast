from django.shortcuts import render
from django.utils.timezone import now
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from reporting.reports.test import DummyExpenseReport
from django.http import HttpResponse
from reporting.reports.test import DummyExpenseReport  # adjust if path is different


User = get_user_model()

class ExpenseReportHTMLPreviewView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # ✅ Force a test user (admin@gmail.com)
        test_user = get_object_or_404(User, email="admin@gmail.com")

        # ✅ Use your report with the test user
        report = DummyExpenseReport(filters={}, user=test_user)
        context = report.get_test_context()

        return render(request, "reports/test.html", context)
    




def test_expense_report_view(request):
    test_user = get_object_or_404(User, email="admin@gmail.com")
    # Use DummyExpenseReport for testing
    report = DummyExpenseReport(user=test_user,filters={})
    context = report.get_test_context()
   
    # Render PDF using your working BaseReport.render_pdf method
    pdf = report.render_pdf("reports/test.html", context)

    # Return PDF in browser
    response = HttpResponse(pdf, content_type="application/pdf")

    # Optional: Allow inline preview or download with query param
    if request.GET.get("download") == "1":
        response["Content-Disposition"] = 'attachment; filename="test_expense_report.pdf"'
    else:
        response["Content-Disposition"] = 'inline; filename="test_expense_report.pdf"'

    return response



def my_html_view(request):
    context = {
        "title": "Welcome",
        "message": "This is a rendered HTML page from a Django view.",
    }
    return render(request, "reporting/reciept.html", context)
