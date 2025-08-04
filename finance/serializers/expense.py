from rest_framework import serializers
from finance.models.expense_category import ExpenseCategory
from finance.models.expense_item import ExpenseItem
from finance.models.expense_item_attachment import ExpenseItemAttachment
from django.utils.timezone import now
from django.db.models import Sum
from datetime import timedelta

class ExpenseCategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = ExpenseCategory
        fields = [
            "id",
            "name",
            "code",
            "type",
            "monthly_budget",
            "description",
            "image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["farm"] = self.context["request"].user.active_farm
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.type = validated_data.get('type', instance.type)
        instance.monthly_budget = validated_data.get('monthly_budget', instance.monthly_budget)
        instance.description = validated_data.get('description', instance.description)

        image = validated_data.get('image', None)
        if image is not None:
            instance.image = image

        instance.save()
        return instance

class ExpenseItemAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseItemAttachment
        fields = ["id", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]

class ExpenseItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    attachments = ExpenseItemAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = ExpenseItem
        fields = [
            "id",
            "category",
            "category_name",
            "code",
            "label",
            "amount",
            "description",
            "status",
            "date",
            "attachments",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "category_name", "attachments"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["farm"] = request.user.active_farm

        category = validated_data["category"]
        amount = validated_data["amount"]
        expense_date = validated_data.get("date") or now().date()

        # Compute first and last day of current month
        first_day = expense_date.replace(day=1)
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # Total spent in this category this month
        total_spent = (
            ExpenseItem.objects.filter(
                category=category,
                farm=request.user.active_farm,
                date__range=(first_day, last_day)
            )
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        new_total = total_spent + amount

        # Create instance
        instance = super().create(validated_data)

        # If monthly budget is set and exceeded, handle it
        if category.monthly_budget and new_total > category.monthly_budget:
            self.handle_budget_exceeded(instance, category, new_total)

        return instance

    def handle_budget_exceeded(self, expense: ExpenseItem, category: ExpenseCategory, total_spent: float):
        """
        Called when monthly budget is exceeded. Attach data to instance for response.
        """
        print("⚠️ Monthly budget exceeded!")
        print(f"Category: {category.name}")
        print(f"Budget: {category.monthly_budget}, Spent: {total_spent}")

        expense._budget_exceeded = True
        expense._budget_info = {
            "category": category.name,
            "monthly_budget": float(category.monthly_budget),
            "total_spent": float(total_spent),
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if hasattr(instance, "_budget_exceeded") and instance._budget_exceeded:
            data["budget_exceeded"] = True
            data["budget_info"] = instance._budget_info

        return data
