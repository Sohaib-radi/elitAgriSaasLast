from django.urls import path, include
from rest_framework.routers import DefaultRouter
from animal.views.animal import AnimalViewSet
from animal.views.list import AnimalListViewSet
from animal.views.image import AnimalImageUploadView
from animal.views.birth import AnimalBirthViewSet
from animal.views.birth import MoveBirthToAnimalView
from animal.views.death import AnimalDeathViewSet
from animal.views.death_image import UploadDeathImageView
from animal.views.vaccine import AnimalVaccineViewSet
from animal.views.recommendation import VaccineRecommendationViewSet
from animal.views.field import CustomListFieldViewSet


router = DefaultRouter()
router.register("animals", AnimalViewSet, basename="animal")
router.register("lists", AnimalListViewSet, basename="animal-list")
router.register("births", AnimalBirthViewSet, basename="animal-birth")
router.register("deaths", AnimalDeathViewSet, basename="animal-death")
router.register("vaccines", AnimalVaccineViewSet, basename="animal-vaccines")
router.register("vaccine-recommendations", VaccineRecommendationViewSet, basename="vaccine-recommendations")
router.register("custom-fields", CustomListFieldViewSet, basename="custom-fields")


urlpatterns = [
    path("", include(router.urls)),
    path("animals/<int:pk>/upload-image/", AnimalImageUploadView.as_view(), name="animal-upload-image"),
    path("births/<int:pk>/move-to-animal/", MoveBirthToAnimalView.as_view(), name="move-birth-to-animal"),
    path("deaths/<int:pk>/upload-images/", UploadDeathImageView.as_view(), name="upload-death-images"),
    
]
