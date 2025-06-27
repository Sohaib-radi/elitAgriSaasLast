from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from product_catalogue.models import Product, PersonalProduct, Project
from product_catalogue.serializers.project import ProjectSerializer
from product_catalogue.serializers.product import ProductSerializer


class PersonalProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    project = ProjectSerializer()

    class Meta:
        model = PersonalProduct
        fields = [
            "id",
            "project",
            "product",
            "quantity",
            "notes",
            "created_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "created_by"]


class PersonalProductCreateSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(
    queryset=Project.objects.all(),
    error_messages={"does_not_exist": _("Project not found.")},
)
    product = serializers.JSONField(required=True)  # will allow full object or int
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_product(self, value):
        # ✅ If updating — skip
        if self.instance:
            return value

        if isinstance(value, int):
            try:
                return Product.objects.get(pk=value)
            except Product.DoesNotExist:
                raise serializers.ValidationError(_("Product not found."))

        if isinstance(value, dict):
            required_fields = ["name", "code", "type", "unit", "category", "purpose"]
            for field in required_fields:
                if field not in value:
                    raise serializers.ValidationError(_(f"Field '{field}' is required in product."))
            return value

        raise serializers.ValidationError(_("Invalid product format."))

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        farm = user.active_farm

        project = validated_data.pop("project")
        product_data = validated_data.pop("product")

        with transaction.atomic():
            # ✅ Use existing product or create new one
            if isinstance(product_data, Product):
                product = product_data
            else:
                product, _ = Product.objects.get_or_create(
                    code=product_data["code"],
                    farm=farm,
                    defaults={
                        "name": product_data["name"],
                        "type": product_data["type"],
                        "unit": product_data["unit"],
                        "category_id": product_data["category"],
                        "purpose": product_data["purpose"],
                        "price": product_data.get("price"),
                        "cost_price": product_data.get("cost_price"),
                        "margin_percentage": product_data.get("margin_percentage"),
                        "weight": product_data.get("weight"),
                        "description": product_data.get("description", ""),
                        "benefit": product_data.get("benefit", ""),
                        "duration": product_data.get("duration"),
                        "product_age": product_data.get("product_age"),
                        "storage_instructions": product_data.get("storage_instructions", ""),
                        "show_in_store": product_data.get("show_in_store", False),
                        "is_active": product_data.get("is_active", True),
                    },
                )

            if PersonalProduct.objects.filter(project=project, product=product).exists():
                raise serializers.ValidationError({
                    "non_field_errors": [_("This product is already assigned to the selected project.")]
                })

            return PersonalProduct.objects.create(
                farm=farm,
                project=project,
                product=product,
                quantity=validated_data["quantity"],
                notes=validated_data.get("notes", ""),
                created_by=user,
            )

    def update(self, instance, validated_data):
        request = self.context["request"]
        user = request.user
        farm = user.active_farm

        product_data = validated_data.pop("product", None)
        project = validated_data.get("project", instance.project)

        with transaction.atomic():
            # ✅ Update product if provided
            if product_data and isinstance(product_data, dict):
                for attr, value in {
                    "name": product_data.get("name"),
                    "type": product_data.get("type"),
                    "unit": product_data.get("unit"),
                    "category_id": product_data.get("category"),
                    "purpose": product_data.get("purpose"),
                    "price": product_data.get("price"),
                    "cost_price": product_data.get("cost_price"),
                    "margin_percentage": product_data.get("margin_percentage"),
                    "weight": product_data.get("weight"),
                    "description": product_data.get("description", ""),
                    "benefit": product_data.get("benefit", ""),
                    "duration": product_data.get("duration"),
                    "product_age": product_data.get("product_age"),
                    "storage_instructions": product_data.get("storage_instructions", ""),
                    "show_in_store": product_data.get("show_in_store", False),
                    "is_active": product_data.get("is_active", True),
                }.items():
                    if value is not None:
                        setattr(instance.product, attr, value)
                instance.product.save()

            instance.quantity = validated_data.get("quantity", instance.quantity)
            instance.notes = validated_data.get("notes", instance.notes)
            instance.project = project
            instance.save()

        return instance

    def to_representation(self, instance):
        return PersonalProductSerializer(instance).data
