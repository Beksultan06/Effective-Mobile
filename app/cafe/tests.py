from django.test import TestCase
from django.urls import reverse
from app.cafe.models import Order
from unittest.mock import patch
import json

class OrderViewsTest(TestCase):

    def setUp(self):
        # Создание тестового заказа
        self.order_data = {
            "table_number": 1,
            "items": [{"name": "Coffee", "price": 5.0}, {"name": "Cake", "price": 3.0}],
            "status": "pending"
        }
        self.order = Order.objects.create(**self.order_data)

    def test_order_list_view(self):
        """
        Тестирует отображение всех заказов.
        """
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', response.context)

    def test_order_detail_view(self):
        """
        Тестирует отображение деталей заказа.
        """
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['order'], self.order)

    def test_order_update_view(self):
        """
        Тестирует обновление данных заказа.
        """
        url = reverse('order-update', kwargs={'pk': self.order.pk})
        data = {
            'status': 'paid',
            'total_price': '8.0',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект после успешного обновления
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'paid')


    def test_order_delete_view(self):
        """
        Тестирует удаление заказа.
        """
        url = reverse('order-delete', kwargs={'pk': self.order.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект после удаления
        self.assertEqual(Order.objects.count(), 0)

    @patch('requests.get')
    def test_revenue_view(self, mock_get):
        """
        Тестирует расчет выручки через API.
        """
        url = reverse('revenue')
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'total_revenue': 1000,
            'paid_orders': []
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_revenue'], 1000)