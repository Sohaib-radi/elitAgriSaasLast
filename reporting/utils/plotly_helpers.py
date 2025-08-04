import plotly.graph_objects as go
import tempfile
import os
from django.conf import settings
import base64


  
def generate_expense_chart(chart_data):
    """
    Generate a pie chart from chart_data and return absolute image path.
    chart_data = [{ "label": "Animal", "amount": 3400 }, ...]
    """
    labels = [item["label"] for item in chart_data]
    values = [item["amount"] for item in chart_data]

    fig = go.Figure(
        data=[go.Pie(labels=labels, values=values, hole=0.3)],
        layout=go.Layout(title="Expense Breakdown by Type", height=400, width=600)
    )

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        fig.write_image(tmp.name)
        tmp.seek(0)
        encoded = base64.b64encode(tmp.read()).decode("utf-8")
        os.unlink(tmp.name)
        return f"data:image/png;base64,{encoded}"
    

def generate_grouped_expense_chart(months, grouped_data):
    fig = go.Figure()

    # Each type is one series
    for expense_type, values in grouped_data.items():
        fig.add_trace(
            go.Bar(
                x=months,
                y=values,
                name=expense_type
            )
        )

    fig.update_layout(
        barmode='group',
        title=dict(text="Monthly Expenses by Type", x=0.5),
        xaxis=dict(title="Month", tickangle=-45),
        yaxis=dict(title="Amount"),
        height=420,
        width=700,
        margin=dict(t=50, b=80, l=50, r=30),
        font=dict(family="Arial", size=13),
    )

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        fig.write_image(tmp.name)
        tmp.seek(0)
        encoded = base64.b64encode(tmp.read()).decode("utf-8")
        os.unlink(tmp.name)
        return f"data:image/png;base64,{encoded}"