from rest_framework.routers import DefaultRouter, SimpleRouter
from apps.categories.views import CategoryViewSet
from apps.products.views import ProductViewSet
from apps.reviews.views import ReviewViewSet
from apps.orders.views import OrderViewSet
from django.contrib import admin
from django.urls import include, path

Router = DefaultRouter()
Router.register(
    r"categories", CategoryViewSet, basename='category'
)

Router.register(
    r"products", ProductViewSet, basename='product'
)

Router.register(
    r"review", ReviewViewSet, basename='review'
)
Router.register(
    r"orders", OrderViewSet, basename = 'order'
)

urlpatterns = [path('admin/', admin.site.urls)] + Router.urls
