from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView,
                                     RetrieveAPIView)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import requests

from app.cafe.models import Order
from api.serializers import OrderSerializers

class OrderListApiView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['table_number', 'status']

class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

class OrderUpdateAPIView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

class OrderDestroyAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

class OrderRetrieveAPIView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

class RevenueAPIView(APIView):
    """
    Класс для расчета общей выручки за заказы со статусом 'оплачено'.
    """
    def get(self, request):
        api_url = f"{settings.API_BASE_URL}/orders/"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            orders = response.json()
            paid_orders = [order for order in orders if order['status'] == 'paid']
            total_revenue = sum(order['total_price'] for order in paid_orders)
            return Response({
                'total_revenue': total_revenue,
                'paid_orders': paid_orders
            })

        except requests.RequestException as e:
            print(f"Ошибка при запросе к API: {str(e)}")
            return Response({'error': f'Ошибка при запросе к API: {str(e)}'}, status=400)
