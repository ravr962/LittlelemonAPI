"""
URL configuration for Littlelemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from  LittlelemonAPI.views import MenuItemViewSet, OrderViewSet, SimpleOrderViewSet
                            #OrderListCreateView, OrderDetailView  # keeping Order views for now
from LittlelemonAPI import views
from rest_framework.authtoken.views import obtain_auth_token
#from LittlelemonAPI.views import (MenuItemListCreateView, MenuItemDetailView #(MenuListAPIView
#, OrderListCreateAPIView
#,OrderListCreateView, OrderDetailView)
                                  #MenuItemDetailAPIView, OrderDetailAPIView)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import os
from django.conf import settings
from django.conf.urls.static import static
from Littlelemon.settings import BASE_DIR


# router = DefaultRouter()
# router.register(r'menu', MenuItemViewSet, basename='menuitem')
# router.register(r'orders', OrderViewSet, basename='order')
# router.register(r'simple-orders', SimpleOrderViewSet, basename='simpleorder')

schema_view = get_schema_view(
    openapi.Info(
        title="Little Lemon API",
        default_version='v1',
        description="API documentation for v1 and v2",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="you@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),  # or path('api/', views.index) # if you want to keep a landing/index view
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    # path('', include(router.urls)),
    
    # Route all API requests to versioned files
    path('api/v1/', include('LittlelemonAPI.urls_v1')),
    # Future support:
    path('api/v2/', include('LittlelemonAPI.urls_v2')),
    
    # Swagger and Redoc UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    #path('menu/', views.menu_items),  # List or create menu items
    #path('menu/', MenuListAPIView.as_view(), name='menu-list'),
    #path("menu/<int:id>/", MenuItemDetailAPIView.as_view(), name="menu-detail"),
    #path('menu/', MenuItemListCreateView.as_view(), name='menu-list-create'),
    #path('menu/<int:pk>/', MenuItemDetailView.as_view(), name='menu-detail'),
    #path('menu/<int:id>/', views.single_menu_item),  # GET, PUT, DELETE menu item by ID
    #path('orders/', views.orders),  # New: Create + list orders
    #path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    #path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    #path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    #path("orders/<int:id>/", OrderDetailAPIView.as_view(), name="order-detail"),
    #path('orders/<int:id>/', views.single_order),  # New route for retrieving a single order

]

# Serve static files in dev
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # For Render and other prod platforms, make sure STATIC_ROOT is served
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
