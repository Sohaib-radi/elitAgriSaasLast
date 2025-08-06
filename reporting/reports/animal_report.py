# reports/animal_report.py

from reporting.base.base import BaseReport
from reporting.base.base_report import AbstractReport
from animal.models.animal import Animal
from django.template.loader import render_to_string
from django.utils.timezone import localtime
from reporting.utils.render_pdf import render_to_pdf
from reporting.utils.save_report_record import save_report_record

class AnimalReport(BaseReport):
    """
    General animal list report (filters: species, status, date added)
    """
    def fetch(self):
        print("[DEBUG] Filters received:", self.filters)

        queryset = Animal.objects.filter(farm=self.user.active_farm)

        species = self.filters.get("species")
        status = self.filters.get("status")
        gender = self.filters.get("gender")
        start = self.filters.get("start")
        end = self.filters.get("end")

        if species:
            queryset = queryset.filter(species=species)

        if status:
            queryset = queryset.filter(status=status)

        if gender:
            queryset = queryset.filter(gender=gender)

        if start and end:
            queryset = queryset.filter(birth_date__range=[start, end])

        print("[DEBUG] Animal list count:", queryset.count())
        return queryset.select_related("mother", "father", "list")


    def format(self, data):
        animals = []
        for animal in data:
            try:
                birth_date = animal.birth_date.strftime("%Y-%m-%d") if animal.birth_date else "—"

                animals.append({
                    "animal_number": animal.animal_number,
                    "international_number": animal.international_number or "—",
                    "name": animal.name or "—",
                    "species": animal.species,
                    "breed": animal.breed or "—",
                    "gender": animal.gender,
                    "birth_date": birth_date,
                    "status": animal.status,
                    "mother": animal.mother.animal_number if animal.mother else "—",
                    "father": animal.father.animal_number if animal.father else "—",
                    "description": animal.description or "—",
                    "is_purchased": "Yes" if animal.is_purchased else "No",
                })
            except Exception as e:
                print(f"[ERROR] Failed to format animal record: {e}")
        context = self.get_context()
        context.update({
            "animals": animals,
            "filters": self.filters,
            "farm": self.user.active_farm,
        })

        pdf = self.render_pdf("reports/animal_list.html", context)

        save_report_record(
            user=self.user,
            report_type="animal_list",
            report_name="Animal List Report",
            pdf_content=pdf,
            filters=self.filters
        )

        return pdf
