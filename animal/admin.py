from django.contrib import admin
from animal.models.animal import Animal
from animal.models.list import AnimalList
# from animal.models.field import CustomListField
from animal.models.birth import AnimalBirth
from animal.models.death import AnimalDeath, AnimalDeathImage
from animal.models.vaccine import AnimalVaccine
from animal.models.recommendation import VaccineRecommendation
from animal.models.field_value import AnimalCustomFieldValue
from animal.models.field import CustomListField
from animal.models.field_value import AnimalCustomFieldValue

class AnimalCustomFieldValueInline(admin.TabularInline):
    model = AnimalCustomFieldValue
    extra = 0
    readonly_fields = ["field", "value", "created_by"]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False  # Prevent adding manually from admin
    
class CustomListFieldInline(admin.TabularInline):
    model = CustomListField
    extra = 1  # how many blank forms to show
    show_change_link = True
@admin.register(Animal)


class AnimalAdmin(admin.ModelAdmin):
    list_display = ("animal_number", "species", "gender", "birth_date", "farm", "list", "status", "is_active")
    search_fields = ("animal_number", "international_number")
    list_filter = ("species", "status", "is_active", "created_at")
    inlines = [AnimalCustomFieldValueInline]

@admin.register(AnimalList)
class AnimalListAdmin(admin.ModelAdmin):
    list_display = ("name", "farm", "created_by", "created_at")
    search_fields = ("name",)
    inlines = [CustomListFieldInline]



@admin.register(AnimalCustomFieldValue)
class AnimalCustomFieldValueAdmin(admin.ModelAdmin):
    list_display = ("animal", "field", "value", "created_by", "created_at")
    search_fields = ("animal__animal_number", "field__name", "value")


@admin.register(AnimalBirth)
class AnimalBirthAdmin(admin.ModelAdmin):
    list_display = ("animal_number", "species", "birth_datetime", "moved_to_animals", "farm", "created_by")
    search_fields = ("animal_number",)
    list_filter = ("species", "moved_to_animals", "created_at")


@admin.register(AnimalDeath)
class AnimalDeathAdmin(admin.ModelAdmin):
    list_display = ("animal", "death_datetime", "status", "reason", "created_by")
    search_fields = ("animal__animal_number",)
    list_filter = ("status", "death_datetime")


@admin.register(AnimalDeathImage)
class AnimalDeathImageAdmin(admin.ModelAdmin):
    list_display = ("death", "image", "uploaded_at")


@admin.register(AnimalVaccine)
class AnimalVaccineAdmin(admin.ModelAdmin):
    list_display = ("animal", "name", "date_given", "valid_until", "status", "created_by")
    list_filter = ("status", "date_given", "valid_until")
    search_fields = ("name", "animal__animal_number")


@admin.register(VaccineRecommendation)
class VaccineRecommendationAdmin(admin.ModelAdmin):
    list_display = ("species", "vaccine_name", "recommended_age_days")
