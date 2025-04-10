from rest_framework import serializers
from finance.models.expense_category import ExpenseCategory
from finance.models.expense_item import ExpenseItem
from finance.models.expense_item_attachment import ExpenseItemAttachment


class ExpenseCategorySerializer(serializers.ModelSerializer):
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
        validated_data["farm"] = self.context["request"].user.active_farm
        return super().create(validated_data)
