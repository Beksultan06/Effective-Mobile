from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from app.cafe.models import Order
from .forms import OrderForm

def order_list(request):
    """
    Отображает все заказы в таблице
    """
    orders = Order.objects.all()
    return render(request, 'order/order_list.html', {'orders': orders})

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
    Обновляет статус заказа
    """
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status
            order.save()
            return redirect('order-list')

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
