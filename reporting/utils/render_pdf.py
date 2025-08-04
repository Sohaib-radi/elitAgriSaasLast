from django.template.loader import render_to_string
from weasyprint import HTML
from django.utils.encoding import force_str
from django.db.models.query import QuerySet


def make_serializable(value):
    """
    Convert QuerySets, model instances, sets, etc. into JSON-safe values.
    """
    if isinstance(value, QuerySet):
        return list(value.values())
    elif isinstance(value, dict):
        return {k: make_serializable(v) for k, v in value.items()}
    elif isinstance(value, (list, tuple, set)):
        return [make_serializable(v) for v in value]
    elif hasattr(value, "__dict__") and not isinstance(value, str):
        return str(value)
    return value


def render_to_pdf(template_name: str, context: dict) -> bytes:
    """
    Render a Django template into PDF bytes using WeasyPrint.
    """
    serializable_context = make_serializable(context)

    # Render HTML string
    html_string = render_to_string(template_name, serializable_context)

    # Generate PDF from HTML
    pdf_bytes = HTML(string=force_str(html_string)).write_pdf()

    return pdf_bytes
