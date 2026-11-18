from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .serializers import OrderCreateSerializer, OrderListSerializer, OrderUpdateSerializer
from .models import Order, OrderItem
from .services import cancel_order

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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get("status") == Order.Status.CANCELLED:
            if instance.status != Order.Status.CANCELLED:
                cancel_order(instance)
        else:
            serializer.save()

        serializer.instance = instance
        return Response(
            self.get_serializer(instance).data,
            status=status.HTTP_200_OK
        )

