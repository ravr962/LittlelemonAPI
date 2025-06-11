from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse #, HttpResponseNotFound, HttpResponseBadRequest
#from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
from decimal import Decimal
import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import MenuItem, Order
from .serializers import MenuItemSerializer, OrderSerializer, OrderCreateSerializer, SimpleOrderSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (ListModelMixin, CreateModelMixin, 
                                   RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from .permissions import IsOwnerOrReadCreateOnly  # Custom permission
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Create your views here.

@csrf_exempt
def index(request):
    return JsonResponse({'message': 'Welcome to LittleLemon API!'})

class MenuItemViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    #permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price', 'inventory']
    search_fields = ['title']
    ordering_fields = ['price', 'inventory', 'title']
    ordering = ['title']  # default ordering

# class MenuItemListCreateView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class MenuListAPIView(APIView):
    
#     authentication_classes = [TokenAuthentication]  # ⬅️ Use token auth
#     permission_classes = [IsAuthenticated]
    
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [AllowAny()]
#         return [IsAuthenticated()]

#     def get(self, request):
#         search_query = request.GET.get('search')
#         items = MenuItem.objects.all()
#         if search_query:
#             items = items.filter(title__icontains=search_query)
#         serializer = MenuItemSerializer(items, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = MenuItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@csrf_exempt
# @login_required
# def menu_items(request):
#     if request.method == 'GET':
#         search_query = request.GET.get('search')

#         if search_query:
#             items = MenuItem.objects.filter(title__icontains=search_query)
#         else:
#             items = MenuItem.objects.all()
            
#         data = []
#         for item in items:
#             data.append({
#                 'id': item.id,
#                 'title': item.title,
#                 'price': float(item.price),
#                 'inventory': item.inventory
#             })
#         return JsonResponse(data, safe=False)

#     elif request.method == 'POST':
#         try:
#             body = json.loads(request.body)

#             # Step 1: Check for missing fields
#             required_fields = ['title', 'price', 'inventory']
#             missing = [field for field in required_fields if field not in body]
#             if missing:
#                 return JsonResponse(
#                     {'error': f"Missing required field(s): {', '.join(missing)}"},
#                     status=400
#                 )

#             # Step 2: Create the item
#             item = MenuItem(
#                 title=body['title'],
#                 price=Decimal(str(body['price'])),
#                 inventory=body['inventory']
#             )
#             item.save()

#             return JsonResponse({
#                 'id': item.id,
#                 'title': item.title,
#                 'price': float(item.price),
#                 'inventory': item.inventory
#             }, status=201)

#         except (TypeError, json.JSONDecodeError):
#             return HttpResponseBadRequest("Invalid JSON format.")

#         except ValidationError as e:
#             return JsonResponse({'errors': e.message_dict}, status=400)

# def menu_items(request):
#     items = MenuItem.objects.all()
#     data = []
#     for item in items:
#         data.append({
#             'id': item.id,
#             'title': item.title,
#             'price': float(item.price),
#             'inventory': item.inventory
#         })
#     return JsonResponse(data, safe=False)

# class MenuItemDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
#     permission_classes = [IsAuthenticated]
#     lookup_field = 'pk'  # optional if using pk

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class MenuItemDetailAPIView(APIView):
    
#     authentication_classes = [TokenAuthentication] 
#     permission_classes = [IsAuthenticated]
    
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [AllowAny()]
#         return [IsAuthenticated()]

#     def get(self, request, id):
#         item = get_object_or_404(MenuItem, pk=id)
#         serializer = MenuItemSerializer(item)
#         return Response(serializer.data)

#     def put(self, request, id):
#         item = get_object_or_404(MenuItem, pk=id)
#         serializer = MenuItemSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         item = get_object_or_404(MenuItem, pk=id)
#         item.delete()
#         return Response({"message": f"Menu item {id} deleted successfully."}, status=status.HTTP_200_OK)

# @csrf_exempt
# #@login_required
# def single_menu_item(request, id):
#     if request.method == 'GET':
#         try:
#             item = MenuItem.objects.get(pk=id)
#             data = {
#                 'id': item.id,
#                 'title': item.title,
#                 'price': float(item.price),
#                 'inventory': item.inventory
#             }
#             return JsonResponse(data)
#         except MenuItem.DoesNotExist:
#             return HttpResponseNotFound("Menu item not found.")

#     elif request.method == 'PUT':
#         try:
#             body = json.loads(request.body)
#             required_fields = ['title', 'price', 'inventory']
#             missing = [field for field in required_fields if field not in body]
#             if missing:
#                 return JsonResponse(
#                     {'error': f"Missing required field(s): {', '.join(missing)}"},
#                     status=400
#                 )

#             item.title = body['title']
#             item.price = Decimal(str(body['price']))
#             item.inventory = body['inventory']
#             item.save()

#             return JsonResponse({
#                 'id': item.id,
#                 'title': item.title,
#                 'price': float(item.price),
#                 'inventory': item.inventory
#             })

#         except (KeyError, TypeError, json.JSONDecodeError):
#             return HttpResponseBadRequest("Invalid or missing data fields.")
#         except ValidationError as e:
#             return JsonResponse({'errors': e.message_dict}, status=400)
        
#     elif request.method == 'DELETE':
#         try:
#             item = MenuItem.objects.get(pk=id)
#             item.delete()
#             return JsonResponse({'message': f'Menu item {id} deleted successfully.'})
#         except MenuItem.DoesNotExist:
#             return HttpResponseNotFound("Menu item not found.")


# def single_menu_item(request, id):
#     try:
#         item = MenuItem.objects.get(pk=id)
#         data = {
#             'id': item.id,
#             'title': item.title,
#             'price': float(item.price),
#             'inventory': item.inventory
#         }
#         return JsonResponse(data)
#     except MenuItem.DoesNotExist:
#         return HttpResponseNotFound("Menu item not found.")

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    #authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadCreateOnly]  # Apply permissions
    
    # Filtering & search
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_at', 'total', 'user', 'customer_name']
    search_fields = ['customer_name', 'user__username']
    ordering_fields = ['created_at', 'total', 'customer_name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        # Choose serializer based on action
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        # Limit queryset to the user's own orders
        return Order.objects.filter(user=self.request.user)
    
class SimpleOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = SimpleOrderSerializer


    # def create(self, request, *args, **kwargs):
    #     # Validate input using OrderCreateSerializer
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)

    #     # Serialize output using OrderSerializer
    #     order = serializer.instance
    #     output_serializer = OrderSerializer(order, context={'request': request})
    #     return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #     # Assign order to logged-in user and validate item IDs
    #     item_ids = serializer.validated_data['item_ids']
    #     customer_name = serializer.validated_data['customer_name']
    #     menu_items = MenuItem.objects.filter(id__in=item_ids)

    #     if menu_items.count() != len(set(item_ids)):
    #         existing_ids = set(menu_items.values_list("id", flat=True))
    #         missing_ids = [id for id in item_ids if id not in existing_ids]
    #         raise ValidationError({"item_ids": f"Invalid item_ids: {missing_ids}"})

    #     total = sum(item.price for item in menu_items)
    #     order = Order.objects.create(customer_name=customer_name, 
    #                                  total=total, 
    #                                  user=self.request.user  # Set owner!
    #                                  )
    #     order.items.set(menu_items)
    #     serializer.instance = order

# class OrderListCreateView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Order.objects.all()
#     #serializer_class = OrderSerializer
#     serializer_class = OrderCreateSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]
    
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['customer_name', 'total', 'created_at']
#     search_fields = ['customer_name']
#     ordering_fields = ['created_at', 'total']
    
#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return OrderCreateSerializer
#         return OrderSerializer  # used for listing

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         # Force the correct output serializer here:
#         order = serializer.instance
#         output_serializer = OrderSerializer(order)

#         return Response(output_serializer.data, status=status.HTTP_201_CREATED)
#         #return self.create(request, *args, **kwargs)
    
#     def perform_create(self, serializer):
#         item_ids = serializer.validated_data['item_ids']
#         customer_name = serializer.validated_data['customer_name']
#         menu_items = MenuItem.objects.filter(id__in=item_ids)

#         if menu_items.count() != len(set(item_ids)):
#             existing_ids = set(menu_items.values_list("id", flat=True))
#             missing_ids = [id for id in item_ids if id not in existing_ids]
#             raise ValidationError({"item_ids": f"Invalid item_ids: {missing_ids}"})

#         total = sum(item.price for item in menu_items)

#         # Create the order instance
#         order = Order.objects.create(customer_name=customer_name, total=total)
#         order.items.set(menu_items)
#         serializer.instance = order  # crucial so DRF knows the instance that was just created


# class OrderListCreateAPIView(APIView):
#     authentication_classes = [TokenAuthentication] 
#     permission_classes = [IsAuthenticated]
    
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [AllowAny()]
#         return [IsAuthenticated()]

#     def get(self, request):
#         orders = Order.objects.prefetch_related('items').all()
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = OrderCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             customer_name = serializer.validated_data['customer_name']
#             item_ids = serializer.validated_data['item_ids']
#             menu_items = MenuItem.objects.filter(id__in=item_ids)

#             if menu_items.count() != len(set(item_ids)):
#                 existing_ids = set(menu_items.values_list("id", flat=True))
#                 missing_ids = [id for id in item_ids if id not in existing_ids]
#                 return Response(
#                     {"error": f"Invalid item_ids: {missing_ids}"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             total = sum(item.price for item in menu_items)
#             order = Order.objects.create(customer_name=customer_name, total=total)
#             order.items.set(menu_items)

#             return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# @login_required
# def orders(request):
#     if request.method == 'GET':
#         customer_filter = request.GET.get('customer')

#         if customer_filter:
#             all_orders = Order.objects.prefetch_related('items').filter(customer_name__icontains=customer_filter)
#         else:
#             all_orders = Order.objects.prefetch_related('items').all()

#         data = []
#         for order in all_orders:
#             data.append({
#                 'id': order.id,
#                 'customer_name': order.customer_name,
#                 'items': [item.title for item in order.items.all()],
#                 'total': float(order.total),
#                 'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
#             })
#         return JsonResponse(data, safe=False)

#     elif request.method == 'POST':
#         try:
#             body = json.loads(request.body)
#             customer_name = body.get("customer_name")
#             item_ids = body.get("item_ids", [])

#             # Validate presence
#             if not customer_name or not item_ids:
#                 return JsonResponse(
#                     {"error": "Both 'customer_name' and 'item_ids' are required."},
#                     status=400
#                 )

#             # Validate all item_ids are integers
#             if not all(isinstance(id, int) for id in item_ids):
#                 return JsonResponse(
#                     {"error": "All item_ids must be integers."},
#                     status=400
#                 )

#             # Fetch and compare against DB
#             menu_items = MenuItem.objects.filter(id__in=item_ids)
#             if menu_items.count() != len(set(item_ids)):
#                 existing_ids = set(menu_items.values_list("id", flat=True))
#                 missing_ids = [id for id in item_ids if id not in existing_ids]
#                 return JsonResponse(
#                     {"error": f"Invalid item_ids: {missing_ids}"},
#                     status=400
#                 )

#             # Calculate total
#             total = sum(item.price for item in menu_items)

#             # Create and associate items
#             order = Order.objects.create(customer_name=customer_name, total=total)
#             order.items.set(menu_items)

#             return JsonResponse({
#                 "id": order.id,
#                 "customer_name": order.customer_name,
#                 "total": float(order.total),
#                 "items": [item.title for item in menu_items]
#             }, status=201)

#         except (json.JSONDecodeError, TypeError):
#             return JsonResponse(
#                 {"error": "Invalid JSON or data format."},
#                 status=400
#             )

# class OrderDetailView(RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#     lookup_field = 'pk'  # Optional; default is 'pk'

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class OrderDetailAPIView(APIView):
#     authentication_classes = [TokenAuthentication] 
#     permission_classes = [IsAuthenticated]
    
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [AllowAny()]
#         return [IsAuthenticated()]

#     def get(self, request, id):
#         order = get_object_or_404(Order.objects.prefetch_related("items"), pk=id)
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)

#     def delete(self, request, id):
#         order = get_object_or_404(Order, pk=id)
#         order.delete()
#         return Response({"message": f"Order {id} deleted successfully."}, status=status.HTTP_200_OK)

# @csrf_exempt
# @login_required
# def single_order(request, id):
#     if request.method == 'GET':
#         try:
#             order = Order.objects.prefetch_related('items').get(pk=id)
#             data = {
#                 'id': order.id,
#                 'customer_name': order.customer_name,
#                 'total': float(order.total),
#                 'items': [item.title for item in order.items.all()]
#             }
#             return JsonResponse(data)
#         except Order.DoesNotExist:
#             return HttpResponseNotFound("Order not found.")
        
#     elif request.method == 'DELETE':
#         try:
#             order = Order.objects.get(pk=id)
#             order.delete()
#             return JsonResponse({'message': f'Order {id} deleted successfully.'})
#         except Order.DoesNotExist:
#             return HttpResponseNotFound('Order not found.')

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def create_superuser_view(request):
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "adminpass123")
        return JsonResponse({"message": "Superuser created"})
    return JsonResponse({"message": "Superuser already exists"})
