from rest_framework import serializers
from models import Order, OrderItem
from ..products.serializers import ProductShortSerializer
from ..users.serializers import UserSerializer
from ..products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','price', 'amount', 'product']

class OrderItemCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all()
    )
    class Meta:
        model = OrderItem
        fields = ['product', 'amount']

class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields=['id','user', 'on_created', 'status', 'items']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']