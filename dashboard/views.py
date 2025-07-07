from django.utils import timezone
from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from animal.models.animal import Animal, AnimalStatus
from animal.models.birth import AnimalBirth, BirthStatus
from animal.models.death import AnimalDeath, AnimalDeathStatus

from datetime import timedelta
from dateutil.relativedelta import relativedelta

from animal.models.vaccine import AnimalVaccine
from finance.models.expense_item import ExpenseItem
from finance.models.purchase import PurchaseInvoice
from django.db.models import Sum

from finance.models.receipt import Receipt


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        farm = user.active_farm

        now = timezone.now()
        first_day_of_this_month = now.replace(day=1)
        first_day_of_last_month = (first_day_of_this_month - relativedelta(months=1)).replace(day=1)
       
        # ------------------ ANIMALS ------------------
        total_animals = Animal.objects.filter(farm=farm, is_active=True).count()
        last_month_animals = Animal.objects.filter(
            farm=farm,
            is_active=True,
            created_at__gte=first_day_of_last_month,
            created_at__lt=first_day_of_this_month
        ).count()

        percent_animals = ((total_animals - last_month_animals) / last_month_animals * 100) if last_month_animals else 100.0

        animal_chart_categories = []
        animal_chart_series = []
        for i in range(5, -1, -1):
            month_start = (first_day_of_this_month - relativedelta(months=i)).replace(day=1)
            month_end = (month_start + relativedelta(months=1))
            count = Animal.objects.filter(farm=farm, is_active=True, created_at__gte=month_start, created_at__lt=month_end).count()
            animal_chart_categories.append(month_start.strftime('%b'))
            animal_chart_series.append(count)

        # ------------------ ANIMAL BIRTHS ------------------
        total_births = AnimalBirth.objects.filter(
            farm=farm,
            birth_datetime__gte=first_day_of_this_month
        ).count()

        last_month_births = AnimalBirth.objects.filter(
            farm=farm,
            birth_datetime__gte=first_day_of_last_month,
            birth_datetime__lt=first_day_of_this_month
        ).count()

        percent_births = ((total_births - last_month_births) / last_month_births * 100) if last_month_births else 100.0

        birth_chart_categories = []
        birth_chart_series = []
        for i in range(5, -1, -1):
            month_start = (first_day_of_this_month - relativedelta(months=i)).replace(day=1)
            month_end = (month_start + relativedelta(months=1))
            count = AnimalBirth.objects.filter(farm=farm, birth_datetime__gte=month_start, birth_datetime__lt=month_end).count()
            birth_chart_categories.append(month_start.strftime('%b'))
            birth_chart_series.append(count)

        # ------------------ ANIMAL DEATHS ------------------
        total_deaths = AnimalDeath.objects.filter(
            farm=farm,
            status=AnimalDeathStatus.CONFIRMED,
            death_datetime__gte=first_day_of_this_month
        ).count()

        last_month_deaths = AnimalDeath.objects.filter(
            farm=farm,
            status=AnimalDeathStatus.CONFIRMED,
            death_datetime__gte=first_day_of_last_month,
            death_datetime__lt=first_day_of_this_month
        ).count()

        percent_deaths = ((total_deaths - last_month_deaths) / last_month_deaths * 100) if last_month_deaths else 100.0

        death_chart_categories = []
        death_chart_series = []
        for i in range(5, -1, -1):
            month_start = (first_day_of_this_month - relativedelta(months=i)).replace(day=1)
            month_end = (month_start + relativedelta(months=1))
            count = AnimalDeath.objects.filter(farm=farm, status=AnimalDeathStatus.CONFIRMED, death_datetime__gte=month_start, death_datetime__lt=month_end).count()
            death_chart_categories.append(month_start.strftime('%b'))
            death_chart_series.append(count)

        #--------------------- ANIMAL BY SPICIES ---------------

        species_counts = Animal.objects.filter(
                            farm=farm,
                            is_active=True
                        ).values('species').annotate(count=Count('id'))
        species_data = [
                            {
                                "label": item['species'].capitalize(),  # "cow" -> "Cow"
                                "value": item['count']
                            }
                            for item in species_counts
                        ]
        
        # ------------- Vaccine distribution by status ----------------------------------
        # Vaccine distribution by status
        vaccine_status_counts = AnimalVaccine.objects.filter(
                                animal__farm=farm
                            ).values('status').annotate(count=Count('id'))

        total_vaccines = sum(item['count'] for item in vaccine_status_counts)

        vaccine_status_data = [
                                {
                                    "label": item['status'].capitalize(),  # "given" ➔ "Given"
                                    "count": item['count'],                # Total count of this status
                                    "percentage": round((item['count'] / total_vaccines) * 100, 2) if total_vaccines else 0
                                }
                                for item in vaccine_status_counts
                            ]
        
        #--------------------------  FINANCE SAMURY --------------------------
        now = timezone.now()
        first_day_this_month = now.replace(day=1)
        first_day_last_month = (first_day_this_month - relativedelta(months=1)).replace(day=1)

        # ---------------- INCOME (Receipts) ----------------
        income_this_month = Receipt.objects.filter(
            farm=farm,
            date__gte=first_day_this_month,
        ).aggregate(total=Sum('amount'))['total'] or 0

        income_last_month = Receipt.objects.filter(
            farm=farm,
            date__gte=first_day_last_month,
            date__lt=first_day_this_month,
        ).aggregate(total=Sum('amount'))['total'] or 0

        income_percent = ((income_this_month - income_last_month) / income_last_month * 100) if income_last_month else 100

        income_chart_categories = []
        income_chart_series = []

        for i in range(5, -1, -1):
            month_start = (first_day_this_month - relativedelta(months=i)).replace(day=1)
            month_end = month_start + relativedelta(months=1)
            total = Receipt.objects.filter(farm=farm, date__gte=month_start, date__lt=month_end).aggregate(total=Sum('amount'))['total'] or 0
            income_chart_categories.append(month_start.strftime('%b'))
            income_chart_series.append(float(total))

        # ---------------- EXPENSES (ExpenseItems) ----------------
        expenses_this_month = ExpenseItem.objects.filter(
            farm=farm,
            date__gte=first_day_this_month,
            status=ExpenseItem.Status.APPROVED
        ).aggregate(total=Sum('amount'))['total'] or 0

        expenses_last_month = ExpenseItem.objects.filter(
            farm=farm,
            date__gte=first_day_last_month,
            date__lt=first_day_this_month,
            status=ExpenseItem.Status.APPROVED
        ).aggregate(total=Sum('amount'))['total'] or 0

        expenses_percent = ((expenses_this_month - expenses_last_month) / expenses_last_month * 100) if expenses_last_month else 100

        expenses_chart_categories = []
        expenses_chart_series = []

        for i in range(5, -1, -1):
            month_start = (first_day_this_month - relativedelta(months=i)).replace(day=1)
            month_end = month_start + relativedelta(months=1)
            total = ExpenseItem.objects.filter(
                farm=farm,
                date__gte=month_start,
                date__lt=month_end,
                status=ExpenseItem.Status.APPROVED
            ).aggregate(total=Sum('amount'))['total'] or 0
            expenses_chart_categories.append(month_start.strftime('%b'))
            expenses_chart_series.append(float(total))

        # ---------------- PURCHASES (PurchaseInvoice) ----------------
        purchases_this_month = PurchaseInvoice.objects.filter(
            farm=farm,
            date__gte=first_day_this_month,
        ).aggregate(total=Sum('total_amount'))['total'] or 0

        purchases_last_month = PurchaseInvoice.objects.filter(
            farm=farm,
            date__gte=first_day_last_month,
            date__lt=first_day_this_month,
        ).aggregate(total=Sum('total_amount'))['total'] or 0

        purchases_percent = ((purchases_this_month - purchases_last_month) / purchases_last_month * 100) if purchases_last_month else 100

        purchases_chart_categories = []
        purchases_chart_series = []

        for i in range(5, -1, -1):
            month_start = (first_day_this_month - relativedelta(months=i)).replace(day=1)
            month_end = month_start + relativedelta(months=1)
            total = PurchaseInvoice.objects.filter(
                farm=farm,
                date__gte=month_start,
                date__lt=month_end
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            purchases_chart_categories.append(month_start.strftime('%b'))
            purchases_chart_series.append(float(total))

        # Aggregate approved expenses by category for this month
        expenses_by_category_qs = (
            ExpenseItem.objects.filter(
                farm=farm,
                date__gte=first_day_this_month,
                status=ExpenseItem.Status.APPROVED
            )
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        # Format for frontend
        expenses_by_category = [
            {
                "label": item["category__name"],
                "value": float(item["total"])
            }
            for item in expenses_by_category_qs
        ]

        return Response({
            "animals": {
                "total": total_animals,
                "percent": round(percent_animals, 2),
                "chart": {
                    "categories": animal_chart_categories,
                    "series": animal_chart_series
                }
            },
            "animal_births": {
                "total": total_births,
                "percent": round(percent_births, 2),
                "chart": {
                    "categories": birth_chart_categories,
                    "series": birth_chart_series
                }
            },
            "animal_deaths": {
                "total": total_deaths,
                "percent": round(percent_deaths, 2),
                "chart": {
                    "categories": death_chart_categories,
                    "series": death_chart_series
                }
            },
            "finance": {
                "income": {
                    "total": float(income_this_month),
                    "percent": round(income_percent, 2),
                    "chart": {
                        "categories": income_chart_categories,
                        "series": income_chart_series
                    }
                },
                "expenses": {
                    "total": float(expenses_this_month),
                    "percent": round(expenses_percent, 2),
                    "chart": {
                        "categories": expenses_chart_categories,
                        "series": expenses_chart_series
                    }
                },
                "purchases": {
                    "total": float(purchases_this_month),
                    "percent": round(purchases_percent, 2),
                    "chart": {
                        "categories": purchases_chart_categories,
                        "series": purchases_chart_series
                    }
                }
            },
            "animal_species_distribution": species_data,
            "vaccine_status_distribution": vaccine_status_data,
            "expenses_by_category": expenses_by_category,
        })
