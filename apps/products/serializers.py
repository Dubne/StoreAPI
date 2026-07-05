from rest_framework import serializers
from .models import Product
from ..categories.serializers import CategoryShortSerializer
class ProductSerializer(serializers.ModelSerializer):
    category = CategoryShortSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id','title', 'description', 'price', 'inventory', 'category']

class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title']
