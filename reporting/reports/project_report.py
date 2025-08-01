from reporting.base.base_report import AbstractReport
from assets_projects.models.project import Project
from django.template.loader import render_to_string
from reporting.utils.render_pdf import render_to_pdf
from reporting.utils.save_report_record import save_report_record
from django.db.models import Count, Sum

class ProjectReport(AbstractReport):
    """
    General Project report (filters: active, date range)
    """

    def fetch(self):
        queryset = Project.objects.filter(farm=self.user.active_farm)

        is_active = self.filters.get("is_active")
        start = self.filters.get("start")
        end = self.filters.get("end")

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if start and end:
            queryset = queryset.filter(start_date__gte=start, end_date__lte=end)

        queryset = queryset.annotate(
            asset_count=Count("primary_assets", distinct=True),
            cost_count=Count("costs", distinct=True)
        )

        return queryset.select_related("parent_project")

    def format(self, projects):
        formatted = []
        total_cost = 0

        for project in projects:
            total_cost += project.total_costs or 0

            formatted.append({
                "name": project.name,
                "number": project.project_number or "—",
                "code": project.project_code,
                "parent": project.parent_project.name if project.parent_project else "—",
                "start_date": project.start_date.strftime("%Y-%m-%d") if project.start_date else "—",
                "end_date": project.end_date.strftime("%Y-%m-%d") if project.end_date else "—",
                "is_active": "Active" if project.is_active else "Hold",
                "total_costs": f"{project.total_costs:,.2f}",
                "asset_count": project.asset_count,
                "cost_count": project.cost_count,
                "address": project.address or "—",
                "description": project.description or "—"
            })

        context = {
            "projects": formatted,
            "filters": self.filters,
            "farm": self.user.active_farm,
            "summary": {
                "total_projects": len(projects),
                "total_cost": f"{total_cost:,.2f}",
            },
            "user": self.user, 
        }

        html = render_to_string("reports/project_report.html", context)
        pdf = render_to_pdf(html, context)

        save_report_record(
            user=self.user,
            report_type="project_report",
            report_name="Project Report",
            pdf_content=pdf,
            filters=self.filters
        )

        return pdf

