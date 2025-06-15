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

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'code',
            'category', 'category_name',
            'purpose',                     
            'price', 'cost_price', 'margin_percentage', 'profit_margin',
            'weight', 'description', 'benefit', 'duration',
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

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'description']


