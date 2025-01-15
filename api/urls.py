from django.urls import path
from api.views.order import (OrderListApiView,
                             OrderCreateAPIView,
                             OrderUpdateAPIView,
                             OrderDestroyAPIView,
                             OrderRetrieveAPIView,
                             PaidOrdersRevenueAPIView,)

urlpatterns = [
    path('orders/', OrderListApiView.as_view(), name='order-list'),  # Список всех заказов
    path('orders/create/', OrderCreateAPIView.as_view(), name='order-create'),  # Создание нового заказа
    path('orders/<int:pk>/', OrderRetrieveAPIView.as_view(), name='order-detail'),  # Детали заказа по ID
    path('orders/<int:pk>/update/', OrderUpdateAPIView.as_view(), name='order-update'),  # Обновление заказа
    path('orders/<int:pk>/delete/', OrderDestroyAPIView.as_view(), name='order-delete'),  # Удаление заказа
    path('revenue/', PaidOrdersRevenueAPIView.as_view(), name='revenue-api'),
]