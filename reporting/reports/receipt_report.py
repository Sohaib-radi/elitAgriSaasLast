import datetime
from pathlib import Path
from django.utils import timezone
from django.utils.functional import Promise
from django.conf import settings
from finance.models.receipt import Receipt
from reporting.base.base import BaseReport
from reporting.utils.render_pdf import render_to_pdf
from reporting.utils.save_report_record import save_report_record
from reporting.utils.qr_helpers import generate_qr_code
import os

class ReceiptReport(BaseReport):
    """
    Receipt voucher report — generates PDF for a single receipt.
    """

    def make_serializable_filters(self):
        cleaned = {}
        for k, v in self.filters.items():
            if hasattr(v, "pk"):
                cleaned[k] = v.pk
            elif isinstance(v, list):
                cleaned[k] = [item.pk if hasattr(item, "pk") else str(item) for item in v]
            elif isinstance(v, (datetime.datetime, datetime.date)):
                cleaned[k] = v.isoformat()
            elif isinstance(v, Promise):  # gettext_lazy, etc.
                cleaned[k] = str(v)
            else:
                try:
                    cleaned[k] = str(v)
                except Exception:
                    cleaned[k] = None
        return cleaned

    def fetch(self):
        receipt_id = self.filters.get("receipt_id")
        if not receipt_id:
            raise ValueError("Missing receipt_id for report generation.")

        return Receipt.objects.select_related("person").get(id=receipt_id, farm=self.user.active_farm)

    def format(self, receipt):
        serialized_filters = self.make_serializable_filters()
        now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        # 📌 Generate QR code (for receipt number or unique string)
       
        qr_code_path = generate_qr_code(f"Receipt #{receipt.receipt_number}")
        qr_code_url = Path(qr_code_path).resolve().as_uri()
        context = self.get_context()
        context.update({
            "receipt_number": receipt.receipt_number,
            "date": receipt.date.strftime("%Y-%m-%d"),
            "customer_number": receipt.person.id,
            "customer_name": receipt.person.name,
            "amount": f"{receipt.amount:.2f}",
            "description": receipt.description or "—",
            "accountant_signature": receipt.accountant_signature or "",
            "recipient_signature": receipt.recipient_signature or "",
            "filters": serialized_filters,
            "farm": self.user.active_farm,
            "qr_code_url": qr_code_url,
            "generated_by": self.user.get_full_name(),
            "now": now,
        })
        
        
        pdf_content = self.render_pdf("reports/receipt_report.html", context)

        save_report_record(
            user=self.user,
            report_type="receipt",
            report_name=f"Receipt #{receipt.receipt_number}",
            pdf_content=pdf_content,
            filters=serialized_filters
        )
        try:
            if qr_code_path and os.path.exists(qr_code_path):
                os.remove(qr_code_path)
        except Exception as e:
            print(f"[WARN] Failed to delete temp QR code: {e}")
        return pdf_content
