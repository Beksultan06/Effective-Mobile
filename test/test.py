import pytest
from django.urls import reverse
from app.cafe.forms import OrderForm
from app.cafe.models import Order

@pytest.mark.django_db
def test_order_create_get(client):
    """Тест GET-запроса к order_create"""
    url = reverse('order-create')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], OrderForm)

@pytest.mark.django_db
def test_order_create_post_valid_data(client):
    """Тест POST-запроса с валидными данными к order_create"""
    url = reverse('order-create')
    valid_data = {
        'table_number': 5,  # Пример: номер стола
        'items': 'Burger:10\nFries:5',  # Строка с блюдами и ценами
    }
    response = client.post(url, data=valid_data)
    assert response.status_code == 302  # Проверяем редирект
    assert response.url == reverse('order-list')  # Проверяем, что редирект на нужный URL
    assert Order.objects.count() == 1  # Проверяем, что заказ был создан
    order = Order.objects.first()
    # Проверяем правильность данных
    assert order.table_number == valid_data['table_number']
    assert order.items == [{"name": "Burger", "price": 10.0}, {"name": "Fries", "price": 5.0}]  # Сравниваем данные


@pytest.mark.django_db
def test_order_create_post_invalid_data(client):
    """Тест POST-запроса с невалидными данными к order_create"""
    url = reverse('order-create')
    invalid_data = {
        'field1': '',  # Оставляем поле пустым или задаем невалидное значение
        'field2': 'value2',
    }
    response = client.post(url, data=invalid_data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], OrderForm)
    assert response.context['form'].errors  # Проверяем, что есть ошибки формы
    assert Order.objects.count() == 0  # Проверяем, что заказ не был создан
