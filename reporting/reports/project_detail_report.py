import io
import base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reporting.base.base import BaseReport
from assets_projects.models.project import Project
from assets_projects.models.asset import Asset
from assets_projects.models.cost import ProjectCost
from reporting.utils.render_pdf import render_to_pdf
from reporting.utils.save_report_record import save_report_record
from django.template.loader import render_to_string
from django.db.models import Sum, Count
from django.utils.html import strip_tags




class ProjectDetailReport(BaseReport):
    """
    Detailed report for a specific project: overview, assets, costs, optional chart
    """

    def fetch(self):
        project_id = self.filters.get("project_id")
        if not project_id:
            raise ValueError("project_id is required in filters")

        project = Project.objects.select_related("parent_project").get(
            farm=self.user.active_farm,
            id=project_id
        )

        assets = Asset.objects.filter(primary_project=project)
        costs = ProjectCost.objects.filter(project=project)

        return {
            "project": project,
            "assets": assets,
            "costs": costs,
        }

    def _generate_cost_chart(self, cost_queryset):
        # Group by cost_type
        data = cost_queryset.values("cost_type").annotate(total=Sum("amount"))
        labels = [entry["cost_type"] for entry in data]
        amounts = [float(entry["total"]) for entry in data]

        if not labels or sum(amounts) == 0:
            return None  # Skip empty chart

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(amounts, labels=labels, autopct="%1.1f%%")
        ax.set_title("Cost Breakdown")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close(fig)

        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return image_base64

    def format(self, data):
        project = data["project"]
        assets = data["assets"]
        costs = data["costs"]

        total_asset_value = assets.aggregate(total=Sum("price"))["total"] or 0
        total_cost = costs.aggregate(total=Sum("amount"))["total"] or 0

        asset_data = [{
            "name": a.name,
            "type": a.get_asset_type_display(),
            "purchase_date": a.purchase_date.strftime("%Y-%m-%d") if a.purchase_date else "—",
            "price": f"{a.price:,.2f}",
            "lifespan": a.lifespan,
            "supplier": a.supplier.supplier_name if a.supplier else "—",
            "description": strip_tags(a.description or "—"),
        } for a in assets]

        cost_data = [{
            "name": c.name,
            "type": c.get_cost_type_display(),
            "amount": f"{c.amount:,.2f}",
            "asset": c.asset.name if c.asset else "—",
            "description": strip_tags(c.description or "—"),
        } for c in costs]

        chart_base64 = self._generate_cost_chart(costs)

        context = self.get_context()
        context.update({
            "project": project,
            "asset_data": asset_data,
            "cost_data": cost_data,
            "summary": {
                "total_assets": assets.count(),
                "total_asset_value": f"{total_asset_value:,.2f}",
                "total_costs": f"{total_cost:,.2f}",
                "supplier_count": assets.values("supplier").distinct().count(),
            },
            "cost_chart": chart_base64,
            "farm": self.user.active_farm,
            "user": self.user,
        })

        pdf = self.render_pdf("reports/project_detail_report.html", context)
        save_report_record(
            user=self.user,
            report_type="project_detail",
            report_name=f"Project Detail Report - {project.name}",
            pdf_content=pdf,
            filters=self.filters
        )

        return pdf
