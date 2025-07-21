from reporting.models.report import ReportRecord
from datetime import datetime


class ReportService:
    """
    Central handler to run reports.
    """

    @staticmethod
    def run(report_instance, save_record=False) -> bytes:
        try:
            output = report_instance.execute()

            if save_record:
                ReportRecord.objects.create(
                    name=getattr(report_instance, "name", "Unnamed Report"),
                    type=report_instance.__class__.__name__,
                    status=ReportRecord.Status.SUCCESS,
                    created_by=report_instance.user,
                    filters=report_instance.filters,
                    executed_at=datetime.now()
                )

            return output

        except Exception as e:
            if save_record:
                ReportRecord.objects.create(
                    name=getattr(report_instance, "name", "Unnamed Report"),
                    type=report_instance.__class__.__name__,
                    status=ReportRecord.Status.FAILED,
                    created_by=report_instance.user,
                    filters=report_instance.filters
                )
            raise e
