from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from core.permissions import IsOwner, ReadOnly, IsOwnerOrAdmin, SAFE_METHODS
from .serializers import OrderCreateSerializer, OrderItemSerializer,OrderItemCreateSerializer, OrderListSerializer, OrderUpdateSerializer
from .models import Order, OrderItem

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    http_method_names = ['get', 'post', 'patch', 'head']
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if not self.request.user.is_staff:
            return Order.objects.filter(user=self.request.user)
        return super().get_queryset()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderListSerializer
        elif self.action in ['create']:
            return OrderCreateSerializer
        elif self.action in ['partial_update']:
            return OrderUpdateSerializer
        return OrderListSerializer
    
    def get_permissions(self):
        if self.action in ['partial_update']:
            return [IsAdminUser()]
        return super().get_permissions()
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
    


