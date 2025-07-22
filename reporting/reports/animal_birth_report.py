# reports/animal_birth_report.py

from reporting.base.base_report import AbstractReport
from django.template.loader import render_to_string
from django.utils.timezone import localtime
from animal.models.birth import AnimalBirth
from reporting.utils.render_pdf import render_to_pdf
from reporting.utils.save_report_record import save_report_record

class AnimalBirthReport(AbstractReport):
    """
    Report for animal births, filtered by date range and species.
    """
    def fetch(self):
        print("[DEBUG] Filters received:", self.filters)

        queryset = AnimalBirth.objects.filter(farm=self.user.active_farm)
        print("[DEBUG] Initial count:", queryset.count())

        start = self.filters.get("start")
        end = self.filters.get("end")
        status = self.filters.get("status")   # newborn status
        gender = self.filters.get("gender")   # newborn gender
        species = self.filters.get("species") # species of baby (if stored directly)

        if start and end:
            print(f"[DEBUG] Filtering by birth_datetime: {start} to {end}")
            queryset = queryset.filter(birth_datetime__date__range=[start, end])

        if status:
            print(f"[DEBUG] Filtering by status: {status}")
            queryset = queryset.filter(status=status)

        if gender:
            print(f"[DEBUG] Filtering by gender: {gender}")
            queryset = queryset.filter(gender=gender)

        if species:
            print(f"[DEBUG] Filtering by species: {species}")
            queryset = queryset.filter(species=species)

        print("[DEBUG] Final queryset count:", queryset.count())
        return queryset

    def format(self, data):
        births = []
        for birth in data:
            try:
                formatted_date = localtime(birth.birth_datetime).strftime("%Y-%m-%d %H:%M")

                births.append({
                    "animal_number": birth.animal_number,
                    "international_number": birth.international_number or "—",
                    "species": birth.species,
                    "gender": birth.gender,
                    "birth_date": formatted_date,
                    "status": birth.status,
                    "moved_to_animals": "Yes" if birth.moved_to_animals else "No",
                    "description": birth.description or "—"
                })
            except Exception as e:
                print(f"[ERROR] Birth record failed: {e}")

        context = {
            "births": births,
            "filters": self.filters,
            "farm": self.user.active_farm,
        }

        html = render_to_string("reports/animal_birth.html", context)
        pdf_content = render_to_pdf(html, context)

        save_report_record(
            user=self.user,
            report_type="animal_birth",
            report_name="Animal Birth Report",
            pdf_content=pdf_content,
            filters=self.filters
        )

        return pdf_content
