from rest_framework.routers import DefaultRouter, SimpleRouter
from apps.categories.views import CategoryViewSet
from apps.products.views import ProductViewSet
from apps.reviews.views import ReviewViewSet
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
urlpatterns = [path('admin/', admin.site.urls)] + CategoryRouter.urls + ProductRouter.urls + ReviewRouter.urls
