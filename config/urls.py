from rest_framework.routers import DefaultRouter, SimpleRouter
from apps.categories.views import CategoryViewSet
from django.contrib import admin
from django.urls import include, path

CategoryRouter = DefaultRouter()
CategoryRouter.register(
    r"categories", CategoryViewSet, basename='category'
)

urlpatterns = [path('admin/', admin.site.urls)] + CategoryRouter.urls
