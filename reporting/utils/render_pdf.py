from django.template.loader import render_to_string
import requests
from collections.abc import Iterable
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


def render_to_pdf(template_str: str, context: dict) -> bytes:
    serializable_context = make_serializable(context)

    response = requests.post(
        "http://localhost:5000/pdf",
        json={
            "template": template_str,
            "context": serializable_context,
        },
    )
    if response.status_code == 200:
        return response.content
    raise Exception(f"PDF generation failed: {response.text}")
