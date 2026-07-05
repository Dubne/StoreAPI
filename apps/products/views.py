from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from core.permissions import IsOwner, ReadOnly
from .serializers import ProductSerializer
from .models import Product

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser | ReadOnly]


