# LittlelemonAPI/urls_v1.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MenuItemViewSet, OrderViewSet, SimpleOrderViewSet

router = DefaultRouter()
router.register(r'menu', MenuItemViewSet, basename='menuitem')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'simple-orders', SimpleOrderViewSet, basename='simpleorder')

urlpatterns = [
    path('', include(router.urls)),
]
