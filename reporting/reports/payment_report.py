import os
import datetime
from pathlib import Path
from django.utils import timezone
from django.utils.functional import Promise
from reporting.base.base import BaseReport
from reporting.utils.qr_helpers import generate_qr_code
from reporting.utils.save_report_record import save_report_record
from finance.models.payment import Payment


class PaymentReport(BaseReport):
    """
    💸 Payment voucher report — generates PDF for a single payment.
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
            elif isinstance(v, Promise):
                cleaned[k] = str(v)
            else:
                try:
                    cleaned[k] = str(v)
                except Exception:
                    cleaned[k] = None
        return cleaned

    def fetch(self):
        payment_id = self.filters.get("payment_id")
        if not payment_id:
            raise ValueError("Missing payment_id for report generation.")

        return Payment.objects.select_related("person").get(id=payment_id, farm=self.user.active_farm)

    def format(self, payment):
        serialized_filters = self.make_serializable_filters()
        now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        qr_code_path = generate_qr_code(f"Payment #{payment.payment_number}")
        qr_code_url = Path(qr_code_path).resolve().as_uri()

        context = self.get_context()
        context.update({
            "payment_number": payment.payment_number,
            "date": payment.date.strftime("%Y-%m-%d"),
            "recipient_number": payment.person.id,
            "recipient_name": payment.person.name,
            "amount": f"{payment.amount:.2f}",
            "description": payment.description or "—",
            "accountant_signature": payment.accountant_signature or "",
            "recipient_signature": payment.recipient_signature or "",
            "filters": serialized_filters,
            "farm": self.user.active_farm,
            "qr_code_url": qr_code_url,
            "generated_by": self.user.get_full_name(),
            "now": now,
        })

        pdf_content = self.render_pdf("reports/payment_report.html", context)

        save_report_record(
            user=self.user,
            report_type="payment",
            report_name=f"Payment #{payment.payment_number}",
            pdf_content=pdf_content,
            filters=serialized_filters
        )

        try:
            if qr_code_path and os.path.exists(qr_code_path):
                os.remove(qr_code_path)
        except Exception as e:
            print(f"[WARN] Failed to delete temp QR code: {e}")

        return pdf_content
