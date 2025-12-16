from django.urls import reverse
from django.db import transaction
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from cart.utils import Cart, cap_cat_qs
from order.models import Cap, Order, CapOrder


@login_required
def cart_detail(request: HttpRequest) -> HttpResponse:
    """ Full cart view. """
    cart = Cart(request)
    return render(request, "cart/index.html", {
        "cart": cart,
        "cart_items": cart.items,
    })

@login_required
@require_POST
def cart_order(request: HttpRequest):
    with transaction.atomic():
        cart = Cart(request)
        # Create the order
        order = Order.objects.create(
            customer=request.user, 
            shipping_address=str(request.POST.get('shipping-address'))
        )
        
        # Create the related CapOrder objects
        cap_orders = [
            CapOrder(
                order=order,
                cap=item.get("cap"),
                quantity=item.get('quantity'),
            ) for item in cart.items
        ]
        # Bulk create for efficiency
        CapOrder.objects.bulk_create(cap_orders)
        cart.clear()

        return redirect(reverse('cart:my-order', kwargs={
            "order_id": order.pk
        }))

@login_required
def my_orders(request: HttpRequest):
    orders = (
        Order.objects
        .select_related("customer")
        .prefetch_related("caps")
        .filter(customer=request.user)
    )

    page = int(request.GET.get("page", 1))
    paginator = Paginator(orders, 15)

    return render(request, "orders/list.html", {
        "orders": paginator.get_page(page)
    })

@login_required
def my_order(request: HttpRequest, order_id: int):
    order_qs = Order.objects.prefetch_related(Prefetch(
        'cap_orders', CapOrder.objects.select_related('cap__category')
    ))
    order = get_object_or_404(order_qs, pk=order_id, customer=request.user)

    return render(request, 'orders/detail.html', {
        'order': order
    })

@login_required
@require_POST
def cart_remove(request: HttpRequest, cap_id: int) -> HttpResponse:
    cap = get_object_or_404(Cap.objects.only('id'), pk=cap_id)
    cart = Cart(request)
    cart.toggle(cap.pk)

    return render(request, "htmx/cart-count.html", {
        'cart': cart
    })


@require_POST
def cart_toggle(request: HttpRequest, cap_id: int) -> HttpResponse:
    cap = get_object_or_404(Cap.objects.only('id'), pk=cap_id)
    cart = Cart(request)
    cart.toggle(cap.pk)

    return render(request, "htmx/cart-toggler.html", {
        "cap": cap, "oob": True
    })

@login_required
@require_POST
def cart_increase(request: HttpRequest, cap_id: int) -> HttpResponse:
    cap = get_object_or_404(cap_cat_qs, pk=cap_id)
    cart = Cart(request)
    cart.increase(cap_id)

    return render(request, "htmx/cart-item.html", {
        "item": cart.get_item(cap),
        'cart': cart, 'oob': True
    })


@login_required
@require_POST
def cart_decrease(request: HttpRequest, cap_id: int) -> HttpResponse:
    cap = get_object_or_404(cap_cat_qs, pk=cap_id)
    cart = Cart(request)
    cart.decrease(cap_id)

    return render(request, "htmx/cart-item.html", {
        "item": cart.get_item(cap),
        'cart': cart, 'oob': True
    })


@login_required
@require_POST
def cart_clear(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    cart.clear()

    return redirect('home')
