from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import urllib.parse
from app.cafe.models import Order
from .forms import OrderForm
from django.conf import settings
import requests


def order_list(request):
    """
    Отображает все заказы с использованием API без пагинации.
    """
    api_url = f"{settings.API_BASE_URL}/api/orders/"
    search_query = request.GET.get('search', '')
    params = {
        'search': search_query,
    }

    try:
        response = requests.get(api_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Выводим данные, чтобы увидеть, что приходит от API
        print("API Response:", data)

        # Если data — это список, то присваиваем его переменной orders
        if isinstance(data, list):
            orders = data
        else:
            orders = data.get('results', [])

    except requests.RequestException as e:
        print(f"Ошибка API: {e}")
        orders = []

    return render(request, 'order/order_list.html', {
        'orders': orders,
        'search_query': search_query,
    })

def order_create(request):
    """
    Обрабатывает создание нового заказа
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order-list')
    else:
        form = OrderForm()

    return render(request, 'order/order_create.html', {'form': form})

def order_detail(request, pk):
    """
    Отображает детали заказа по ID
    """
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order/order_detail.html', {'order': order})

def order_update(request, pk):
    """
    Обновляет данные заказа, кроме номера стола.
    """
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_customer_name = request.POST.get('customer_name')
        new_status = request.POST.get('status')
        new_total_price = request.POST.get('total_price')
        if new_customer_name:
            order.customer_name = new_customer_name
        if new_status:
            order.status = new_status
        if new_total_price:
            try:
                order.total_price = float(new_total_price)
            except ValueError:
                messages.error(request, "Неверная сумма заказа.")
                return render(request, 'order/order_update.html', {'order': order})
        try:
            order.save()
            messages.success(request, "Заказ успешно обновлен.")
            return redirect('order-list')
        except Exception as e:
            messages.error(request, f"Ошибка при сохранении заказа: {str(e)}")
            return render(request, 'order/order_update.html', {'order': order})

    return render(request, 'order/order_update.html', {'order': order})


def order_delete(request, pk):
    """
    Удаляет заказ
    """
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order-list')
    return render(request, 'order/order_delete.html', {'order': order})


def revenue(request):
    """
    Расчет общего объема выручки за заказы со статусом 'оплачено'.
    Данные берутся через API, созданное через PaidOrdersRevenueAPIView.
    """
    api_url = f"{settings.API_BASE_URL}/api/revenue/"
    try:
        response = requests.get(api_url)
        print(f"API Response: {response.text}")
        response.raise_for_status()
        if not response.text.strip():
            print("API вернул пустой ответ.")
            total_revenue = 0
            paid_orders = []
        else:
            data = response.json()
            if 'error' in data:
                print(f"Ошибка от API: {data['error']}")
                total_revenue = 0
                paid_orders = []
            else:
                total_revenue = data.get('total_revenue', 0)
                paid_orders = data.get('paid_orders', [])

    except requests.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        total_revenue = 0
        paid_orders = []

    return render(request, 'revenue.html', {'total_revenue': total_revenue, 'paid_orders': paid_orders,})

def errors(request, exception):
    return render(request, "404/404.html", status=404)