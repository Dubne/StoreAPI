from rest_framework import serializers
from .models import Order, OrderItem
from ..products.serializers import ProductShortSerializer
from ..users.serializers import UserSerializer
from ..products.models import Product
from .services import create_order

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
        fields=['id','user', 'on_created', 'status','total_price', 'items']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)
    class Meta:
        model = Order
        fields = ['items']

    def create(self, validated_data):
        return create_order(
            user=self.context["request"].user,
            data=validated_data
        )
    
class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']