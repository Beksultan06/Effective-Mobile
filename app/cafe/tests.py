from django.test import TestCase
from django.urls import reverse
from app.cafe.models import Order
from unittest.mock import patch

class OrderModelTest(TestCase):

    def setUp(self):
        # Создание данных для заказа
        self.order_data = {
            "table_number": 1,
            "items": [{"name": "Coffee", "price": 5.0}, {"name": "Cake", "price": 3.0}],
            "status": "pending"
        }
        # Создаем заказ в базе данных
        self.order = Order.objects.create(**self.order_data)

    def test_order_creation(self):
        """
        Тест проверяет корректность создания заказа и правильность значений его атрибутов.
        """
        order = self.order
        self.assertEqual(order.table_number, 1)  # Проверка номера стола
        self.assertEqual(len(order.items), 2)  # Проверка количества товаров в заказе
        self.assertEqual(order.total_price, 8.0)  # Проверка общей стоимости заказа
        self.assertEqual(order.status, 'pending')  # Проверка статуса заказа
        self.assertEqual(str(order), f"Заказ #{order.id} - Стол #{order.table_number} ({order.status})")  # Проверка строки для __str__ метода

class OrderListViewTest(TestCase):

    def setUp(self):
        # Создание данных для заказа
        self.order_data = {
            "table_number": 1,
            "items": [{"name": "Coffee", "price": 5.0}, {"name": "Cake", "price": 3.0}],
            "status": "pending"
        }
        # Создаем заказ в базе данных
        self.order = Order.objects.create(**self.order_data)

    def test_order_list_view(self):
        """
        Тест проверяет правильность отображения всех заказов в представлении order_list.
        """
        url = reverse('order-list')  # Формируем URL для представления order-list
        response = self.client.get(url)  # Делаем GET-запрос
        self.assertEqual(response.status_code, 200)  # Статус код должен быть 200 (OK)
        self.assertIn('orders', response.context)  # В контексте ответа должен быть ключ 'orders'
        self.assertEqual(len(response.context['orders']), 7)  # Проверяем, что количество заказов равно 7 (это зависит от вашей базы данных)

    @patch('requests.get')
    def test_order_list_view_api(self, mock_get):
        """
        Тест проверяет работу представления order_list с мокированным API.
        """
        url = reverse('order-list')  # Формируем URL для представления order-list
        # Мокируем ответ от API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'results': [
                {
                    'id': self.order.id,
                    'table_number': self.order.table_number,
                    'items': self.order.items,
                    'total_price': self.order.total_price,
                    'status': self.order.status,
                }
            ]
        }

        response = self.client.get(url)  # Делаем GET-запрос
        self.assertEqual(response.status_code, 200)  # Статус код должен быть 200 (OK)
        self.assertIn('orders', response.context)  # В контексте ответа должен быть ключ 'orders'
        self.assertEqual(len(response.context['orders']), 1)  # Проверяем, что количество заказов в ответе равно 1 (поскольку мы мокируем один заказ)
        self.assertEqual(response.context['orders'][0]['id'], self.order.id)  # Проверяем, что ID заказа соответствует мокированному

    def test_order_list_search_view(self):
        """
        Тест проверяет работу поиска в представлении order_list.
        """
        url = reverse('order-list') + '?search=Coffee'  # Формируем URL с параметром поиска 'Coffee'
        response = self.client.get(url)  # Делаем GET-запрос
        self.assertEqual(response.status_code, 200)  # Статус код должен быть 200 (OK)
        self.assertIn('orders', response.context)  # В контексте ответа должен быть ключ 'orders'
        orders = response.context['orders']
        self.assertEqual(len(orders), 0)  # Проверяем, что список заказов пуст, так как таких заказов нет в базе данных
