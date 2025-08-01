from rest_framework import serializers
from product_catalogue.models import Product, ProductCategory, ProductImage, ProductVariant

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'uploaded_at']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'code', 'name', 'weight', 'packaging', 'description', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    farm = serializers.PrimaryKeyRelatedField(read_only=True)
    profit_margin = serializers.SerializerMethodField()
    code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'code',
            'category', 'category_name',
            'purpose',                     
            'price', 'cost_price', 'margin_percentage', 'profit_margin',
            'weight', 'description', 'benefit', 'duration','efficiency_time',	
            'product_age', 'storage_instructions',
            'is_active', 'show_in_store',
            'created_at',
            'images', 'variants', 'farm',
            'type'
        ]
        read_only_fields = [
            'id', 'created_at', 'profit_margin',
            'images', 'variants', 'category_name'
        ]

    def get_profit_margin(self, obj):
        return obj.profit_margin
    
    def create(self, validated_data):
        if not validated_data.get('code'):
            validated_data['code'] = self.generate_product_code(validated_data)
        return super().create(validated_data)

    def generate_product_code(self, data):
        type_prefix = {
            'medicine': 'MED',
            'animal': 'ANI',
            'agricultural': 'AGR',
            'raw_material': 'RAW',
            'other': 'OTH',
        }.get(data.get('type', ''), 'PRD')

        last = (
            Product.objects.filter(type=data['type'])
            .order_by('id')
            .last()
        )
        next_id = (last.id + 1) if last else 1
        return f"{type_prefix}-{next_id:04d}"

    def validate(self, data):
        type_ = data.get("type") or getattr(self.instance, "type", None)

        # Mapping required fields by type
        required_by_type = {
            "medicine": [
                "name", "weight", "description", "benefit", "duration", "product_age", "storage_instructions"
            ],
            "animal": [
                "name", "weight", "description", "benefit", "product_age", "storage_instructions"
            ],
            "agricultural": [
                "name", "weight", "description","efficiency_time", "benefit", "duration", "product_age", "storage_instructions"
            ],
            "raw_material": [
                "name", "description", "benefit"
            ],
            "other": [
                "name", "description", "benefit"
            ]
        }

        required_fields = required_by_type.get(type_, [])
        missing = []

        for field in required_fields:
            val = data.get(field) or (getattr(self.instance, field, None) if self.instance else None)
            if val in [None, ""]:
                missing.append(field)

        if missing:
            raise serializers.ValidationError({
                "missing_fields": [f"Field '{field}' is required for product type '{type_}'." for field in missing]
            })

        return data

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'description']


