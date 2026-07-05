from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from core.permissions import IsOwner, ReadOnly
from .serializers import CategorySerializer
from .models import Category

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser | ReadOnly]
