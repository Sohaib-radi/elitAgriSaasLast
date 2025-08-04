from django.utils.timezone import now
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from reporting.base.base import BaseReport 


class DummyExpenseReport(BaseReport):
    def fetch(self):
        return {}  # not used in test

    def format(self, data):
        return {}  # not used in test

    def get_test_context(self):
        context = self.get_context()
        context.update({
            "total_amount": "12,455.00",
            "top_type_name": "Feed",
            "top_type_amount": "4,350.00",
            "chart_image_path": "",
            "monthly_chart": "",
            "summary_cards": [
                {"title": "Top Category", "description": "Feed - 4,350.00"},
                {"title": "Average ", "description": "456.25"},
                {"title": "Number of ", "description": "42"},
                {"title": "Largest ", "description": "1,200.00"},
            ],
           
            "expenses": [
                {
                    "date": "2025-06-02",
                    "label": "Veterinary Visit",
                    "amount": "150.00",
                    "category": "Health",
                    "type": "Animal",
                    "status": "Paid",
                },
                {
                    "date": "2025-06-05",
                    "label": "Corn Feed",
                    "amount": "250.00",
                    "category": "Feed",
                    "type": "Animal",
                    "status": "Paid",
                },
                {
                    "date": "2025-06-08",
                    "label": "Fuel for Tractor",
                    "amount": "130.00",
                    "category": "Transport",
                    "type": "Operations",
                    "status": "Pending",
                },
                {
                    "date": "2025-06-11",
                    "label": "Vaccination",
                    "amount": "300.00",
                    "category": "Health",
                    "type": "Animal",
                    "status": "Paid",
                },
                {
                    "date": "2025-06-14",
                    "label": "Machinery Repair",
                    "amount": "1200.00",
                    "category": "Equipment",
                    "type": "Operations",
                    "status": "Paid",
                },
            ]
        })
        return context
