from rest_framework.routers import DefaultRouter, SimpleRouter
from apps.categories.views import CategoryViewSet
from apps.products.views import ProductViewSet
from apps.reviews.views import ReviewViewSet
from apps.orders.views import OrderViewSet
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


Router = DefaultRouter()
Router.register(
    r"api/categories", CategoryViewSet, basename='category'
)

Router.register(
    r"api/products", ProductViewSet, basename='product'
)

Router.register(
    r"api/review", ReviewViewSet, basename='review'
)
Router.register(
    r"api/orders", OrderViewSet, basename = 'order'
)

urlpatterns = [path('admin/', admin.site.urls)] + [
    path("api/token/",TokenObtainPairView.as_view(),name="token_obtain_pair",)] + [
    path("api/token/refresh/",TokenRefreshView.as_view(),name="token_refresh",)] + [
    path("api/", include("djoser.urls")),
    path("api/", include("djoser.urls.jwt"))] + [ 
    path("api/schema/",SpectacularAPIView.as_view(),name="schema")] + [
    path("api/docs/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui")] + Router.urls

