from rest_framework import serializers
from .models import Order, OrderItem
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
        fields=['id','user', 'on_created', 'status','total_price', 'items']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)
    class Meta:
        model = Order
        fields = ['items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        request = self.context["request"]
        order = Order.objects.create(user=request.user)
        for item in items_data:
            OrderItem.objects.create(order=order, product=item["product"], amount=item["amount"] )
        return order

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']