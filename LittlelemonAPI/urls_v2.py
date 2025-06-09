from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views_v2 import MenuItemV2ViewSet, OrderV2ViewSet

router = DefaultRouter()
router.register(r'menu', MenuItemV2ViewSet, basename='menuitem-v2')
router.register(r'orders', OrderV2ViewSet, basename='order-v2')

urlpatterns = [
    path('', include(router.urls)),
]
