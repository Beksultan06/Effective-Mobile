from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView,
                                     RetrieveAPIView)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

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