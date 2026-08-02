from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from core.permissions import IsOwner, ReadOnly, IsOwnerOrAdmin
from .serializers import ReviewSerializer
from .models import Review
from .services import create_review

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        review = create_review(serializer.validated_data,self.request.user)
        serializer.instance = review
        
        

