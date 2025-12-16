from django.http import HttpRequest
from django.db.models import Q, Prefetch
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from app.decorators import staff_required
from order.models import Order, CapOrder


@staff_required
def orders(request: HttpRequest):
    orders = Order.objects.select_related("customer").prefetch_related("caps")

    q = request.GET.get("q")
    status = request.GET.get("status")

    if q:
        orders = orders.filter(
            Q(customer__username__icontains=q) |
            Q(customer__first_name__icontains=q) |
            Q(customer__last_name__icontains=q)
        )

    if status:
        orders = orders.filter(status=status)

    paginator = Paginator(orders, 15)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "orders/list.html", {
        "orders": page_obj,
        "page_obj": page_obj,
        "statuses": Order.STATUS_CHOICES,
    })

@staff_required
def order(request: HttpRequest, pk: int):
    order_qs = Order.objects.prefetch_related(Prefetch(
        'cap_orders', CapOrder.objects.select_related('cap__category')
    ))
    order = get_object_or_404(order_qs, pk=pk)

    return render(request, 'orders/detail.html', {
        'order': order
    })

@staff_required
def update_order(request: HttpRequest): pass
