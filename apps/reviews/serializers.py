from rest_framework import serializers
from .models import Review
from ..products.serializers import ProductShortSerializer
from ..users.serializers import UserSerializer
from ..products.models import Product

class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id','review','mark','created_at', 'product', 'user']
        read_only_fields = ['product', 'user']