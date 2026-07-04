from rest_framework import serializers
from models import Review
from ..products.serializers import ProductShortSerializer
from ..users.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id','review','mark','created_at', 'product', 'user']