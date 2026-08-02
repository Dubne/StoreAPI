from rest_framework import serializers
from .models import Product
from ..categories.serializers import CategoryShortSerializer
from ..categories.models import Category
class ProductSerializer(serializers.ModelSerializer):
    category = CategoryShortSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True)
    class Meta:
        model = Product
        fields = ['id','title', 'description', 'price', 'inventory', 'category', 'category_id']

class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title']
