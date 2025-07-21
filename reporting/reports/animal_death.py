from reporting.base.base_report import AbstractReport
from animal.models.death import AnimalDeath
from django.template.loader import render_to_string
from reporting.utils.render_pdf import render_to_pdf
from reporting.utils.save_report_record import save_report_record
from django.utils.timezone import localtime


class AnimalDeathReport(AbstractReport):
    """
    Concrete report for listing animal deaths with filters.
    """

    def fetch(self):
        queryset = AnimalDeath.objects.filter(farm=self.user.active_farm)

        start_date = self.filters.get("start_date")
        end_date = self.filters.get("end_date")
        species = self.filters.get("species")

        if start_date and end_date:
            queryset = queryset.filter(death_datetime__date__range=[start_date, end_date])
        if species:
            queryset = queryset.filter(animal__species=species)

        queryset = queryset.select_related("animal")
        print(f"[DEBUG] Queryset count: {queryset.count()}")  # ✅ Print number of matched records

        return queryset

    def format(self, data):
        deaths = []
        for death in data:
            try:
                print(f"[DEBUG] AnimalDeath ID {death.id}: death_datetime={getattr(death, 'death_datetime', None)}")

                animal = death.animal
                animal_number = animal.animal_number if animal else "—"
                species = animal.species if animal else "—"
                dt = death.death_datetime
                formatted_datetime = localtime(dt).strftime("%Y-%m-%d %H:%M") if dt else "—"
                reason = death.reason
                status = death.status
                print(f"[DEBUG] AnimalDeath ID {death.id}: death_datetime={formatted_datetime}")

                deaths.append({
                    "animal_number": animal_number,
                    "species": species,
                    "death_datetime": formatted_datetime,
                    "status":status,
                    "reason": reason,
                })
            except Exception as e:
                print(f"[ERROR] Failed to process death ID {death.id if death else 'unknown'}: {e}")

        context = {
            "deaths": deaths,
            "filters": self.make_serializable_filters(),
            "farm": self.user.active_farm,
        }

        print("[DEBUG] Context prepared for rendering:", context)

        html = render_to_string("reports/animal_death.html", context)
        pdf_content = render_to_pdf(html, context)

        print(f"[DEBUG] PDF content size: {len(pdf_content)} bytes")

        save_report_record(
            user=self.user,
            report_type="animal_death",
            report_name="Animal Death Report",
            pdf_content=pdf_content,
            filters=context["filters"]
        )

        return pdf_content

    def make_serializable_filters(self):
        cleaned = {}
        for k, v in self.filters.items():
            if hasattr(v, "pk"):
                cleaned[k] = v.pk
            elif isinstance(v, list):
                cleaned[k] = [item.pk if hasattr(item, "pk") else item for item in v]
            elif hasattr(v, "__dict__"):
                cleaned[k] = str(v)
            else:
                cleaned[k] = v
        print(f"[DEBUG] Cleaned filters: {cleaned}")
        return cleaned
