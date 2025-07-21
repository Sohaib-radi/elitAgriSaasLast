from datetime import date
from django.db.models import Count
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from animal.models import (
    Animal,
    AnimalBirth,
    AnimalDeath,
    AnimalVaccine,
    VaccineRecommendation,
    AnimalList,
)
from animal.serializers.birth import AnimalBirthSerializer
from animal.serializers.death import AnimalDeathSerializer
from animal.serializers.vaccine import AnimalVaccineSerializer
from animal.serializers.recommendation import VaccineRecommendationSerializer


class AnimalDashboardView(APIView):
    """
    Animal module dashboard view.
    Returns aggregated stats and recent activity for the dashboard.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        farm = request.user.active_farm
        today = now().date()
        start_of_month = today.replace(day=1)

        # 🔢 Basic stats
        total_animals = Animal.objects.filter(farm=farm).count()
        total_deaths = AnimalDeath.objects.filter(farm=farm).count()
        total_birth = AnimalBirth.objects.filter(farm=farm).count()
        births_this_month = AnimalBirth.objects.filter(farm=farm, birth_datetime__date__gte=start_of_month).count()
        deaths_this_month = AnimalDeath.objects.filter(farm=farm, death_datetime__date__gte=start_of_month).count()
        vaccinated = AnimalVaccine.objects.filter(farm=farm).count()

        # 📊 Species distribution
        species_distribution = list(
            Animal.objects.filter(farm=farm)
            .values("species")
            .annotate(count=Count("id"))
        )

        # 🍼 Recent births (5)
        recent_births_qs = AnimalBirth.objects.filter(farm=farm).order_by("-birth_datetime")[:5]
        recent_births = AnimalBirthSerializer(recent_births_qs, many=True).data

        # 💀 Recent deaths (5)
        recent_deaths_qs = AnimalDeath.objects.filter(farm=farm).order_by("-death_datetime")[:5]
        recent_deaths = AnimalDeathSerializer(recent_deaths_qs, many=True).data

        # 💉 Last vaccinations (5)
        last_vacc_qs = AnimalVaccine.objects.filter(farm=farm).order_by("-date_given")[:5]
        last_vaccinations = AnimalVaccineSerializer(last_vacc_qs, many=True).data

        # ⏰ Vaccinations due (expired or pending/scheduled)
        due_vacc_qs = AnimalVaccine.objects.filter(farm=farm).filter(
            valid_until__lt=date.today()
        ) | AnimalVaccine.objects.filter(
            farm=farm,
            status__in=["pending", "scheduled"]
        )
        due_vacc_qs = due_vacc_qs.distinct().order_by("valid_until")[:10]
        vaccinations_due = AnimalVaccineSerializer(due_vacc_qs, many=True).data

        # 📋 Animal lists
        animal_lists = list(
            AnimalList.objects.filter(farm=farm)
            .annotate(count=Count("animals"))
            .values("id", "name", "count")
        )

        # 🧠 Recommendations (5)
        recs_qs = VaccineRecommendation.objects.all().order_by("-created_at")[:5]
        recommendations = VaccineRecommendationSerializer(recs_qs, many=True).data

        # ✅ Response
        return Response({
            "total_animals": total_animals,
            "total_deaths": total_deaths,
            "total_birth":total_birth,
            "births_this_month": births_this_month,
            "deaths_this_month": deaths_this_month,
            "vaccinated": vaccinated,
            "species_distribution": species_distribution,
            "recent_births": recent_births,
            "recent_deaths": recent_deaths,
            "last_vaccinations": last_vaccinations,
            "vaccinations_due": vaccinations_due,
            "animal_lists": animal_lists,
            "recommendations": recommendations,
        })
