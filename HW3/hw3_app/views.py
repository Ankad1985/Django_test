# views.py

from django.shortcuts import render
from django.utils import timezone
from .models import Client, Order

def index(request):
    return render(request, 'hw3_app/index.html')


def client_order(request, client_id):
    client = Client.objects.get(pk=client_id)

    # Заказы за последние 7 дней (неделю)
    orders_last_7_days = Order.objects.filter(client=client, order_date__gte=timezone.now() - timezone.timedelta(days=7))

    # Заказы за последние 30 дней (месяц)
    orders_last_30_days = Order.objects.filter(client=client, order_date__gte=timezone.now() - timezone.timedelta(days=30))

    # Заказы за последние 365 дней (год)
    orders_last_365_days = Order.objects.filter(client=client, order_date__gte=timezone.now() - timezone.timedelta(days=365))

    # Получаем уникальные товары из всех заказов
    all_products = set()
    for order in [orders_last_7_days, orders_last_30_days, orders_last_365_days]:
        for o in order:
            all_products.update(o.products.all())

    context = {
        'client': client,
        'orders_last_7_days': orders_last_7_days,
        'orders_last_30_days': orders_last_30_days,
        'orders_last_365_days': orders_last_365_days,
        'all_products': all_products,
    }

    return render(request, 'hw3_app/client_order.html', context)
