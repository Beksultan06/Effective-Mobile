from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView,
                                     RetrieveAPIView)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models

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

class PaidOrdersRevenueAPIView(APIView):
    """
    API для подсчета общей выручки по заказам со статусом 'оплачено'.
    """
    def get(self, request):
        paid_orders = Order.objects.filter(status='paid')
        total_revenue = paid_orders.aggregate(total=models.Sum('total_price'))['total'] or 0
        serializer = OrderSerializers(paid_orders, many=True)
        return Response({
            'total_revenue': total_revenue,
            'paid_orders': serializer.data
        })