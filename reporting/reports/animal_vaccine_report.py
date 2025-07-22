# reporting/reports/animal_vaccine_report.py

from reporting.base.base_report import AbstractReport
from animal.models.vaccine import AnimalVaccine
from django.template.loader import render_to_string
from django.utils.timezone import localtime
from reporting.utils.render_pdf import render_to_pdf
from reporting.utils.save_report_record import save_report_record

class AnimalVaccineReport(AbstractReport):
    def fetch(self):
        queryset = AnimalVaccine.objects.filter(farm=self.user.active_farm)

        start = self.filters.get("start")
        end = self.filters.get("end")
        status = self.filters.get("status")

        if start and end:
            queryset = queryset.filter(date_given__range=[start, end])

        if status:
            queryset = queryset.filter(status=status)

        return queryset.select_related("animal")

    def format(self, data):
        vaccines = []
        for item in data:
            try:
                vaccines.append({
                    "animal_number": item.animal.animal_number if item.animal else "—",
                    "vaccine_name": item.name,
                    "date_given": item.date_given.strftime("%Y-%m-%d"),
                    "valid_until": item.valid_until.strftime("%Y-%m-%d"),
                    "status": item.status,
                    "description": item.description or "—",
                })
            except Exception as e:
                print(f"[ERROR] Failed to format vaccine record: {e}")

        context = {
            "vaccines": vaccines,
            "filters": self.filters,
            "farm": self.user.active_farm,
        }

        html = render_to_string("reports/animal_vaccine.html", context)
        pdf = render_to_pdf(html, context)

        save_report_record(
            user=self.user,
            report_type="animal_vaccine",
            report_name="Animal Vaccination Report",
            pdf_content=pdf,
            filters=self.filters
        )

        return pdf
