import os
import uuid
from django.utils import timezone  
from django.core.files.base import ContentFile
from reporting.models.report import ReportRecord
from django.utils.timezone import now

def save_report_record(user, report_type, report_name, pdf_content, filters=None):
    """
    Save a ReportRecord instance with the given data.
    """
    try:
        filename = f"{report_type}_{uuid.uuid4().hex}.pdf"
        file_path = os.path.join("reports", filename)

        record = ReportRecord.objects.create(
            name=report_name,
            type=report_type,
            status=ReportRecord.Status.SUCCESS,
            created_by=user,
            filters=filters or {},
            executed_at=now(),  
        )

        record.file_path.save(filename, ContentFile(pdf_content))
        record.save()

        return record
    except Exception as e:
        ReportRecord.objects.create(
            name=report_name,
            type=report_type,
            status=ReportRecord.Status.FAILED,
            created_by=user,
            filters=filters or {},
            executed_at=timezone.now(),  # ✅ FIXED
        )
        raise e
