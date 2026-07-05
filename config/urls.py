from rest_framework.routers import DefaultRouter, SimpleRouter
from apps.categories.views import CategoryViewSet
from apps.products.views import ProductViewSet
from apps.reviews.views import ReviewViewSet
from apps.orders.views import OrderViewSet
from django.contrib import admin
from django.urls import include, path

CategoryRouter = DefaultRouter()
CategoryRouter.register(
    r"categories", CategoryViewSet, basename='category'
)
ProductRouter = DefaultRouter()
ProductRouter.register(
    r"products", ProductViewSet, basename='product'
)
ReviewRouter = DefaultRouter()
ReviewRouter.register(
    r"review", ReviewViewSet, basename='review'
)
OrderRouter = DefaultRouter()
OrderRouter.register(
    r"orders", OrderViewSet, basename = 'order'
)
urlpatterns = [path('admin/', admin.site.urls)] + CategoryRouter.urls + ProductRouter.urls + ReviewRouter.urls + OrderRouter.urls
