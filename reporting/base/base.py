# reports/base.py

from django.utils import timezone
from reporting.utils.report_utils import get_farm_info  
from .base_report import AbstractReport 
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.conf import settings
import os
from pathlib import Path


class BaseReport(AbstractReport):
    """
    Base report class that provides shared context like farm info, user, and time.
    """

    def get_context(self) -> dict:
        farm = self.user.active_farm if self.user else None
        return {
            "generated_by": f"{self.user.full_name}" if self.user else "System",
            "now": timezone.now(),
            "farm_info": get_farm_info(farm),
        }

    def render_pdf(self, template_name: str, context: dict) -> bytes:
        html = render_to_string(template_name, context)

        media_root = Path(settings.MEDIA_ROOT).resolve()
        base_url = media_root.as_uri()
        css_path = os.path.join(settings.BASE_DIR, "static", "css", "report.css")

        # ❗️ FIX: Set base_url at HTML() level, not just write_pdf()
        html_obj = HTML(string=html, base_url=base_url)

        return html_obj.write_pdf(stylesheets=[CSS(filename=css_path)])