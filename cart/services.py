from django.db import transaction

from cart.utils import Cart
from user.models import User
from payment.models import Payment
from order.models import Order, CapOrder


def make_order(cart: Cart, user: User, shipping_address: str):
    with transaction.atomic():
        # 1. Create the order
        order = Order.objects.create(
            customer=user,
            shipping_address=shipping_address,
        )

        # 2. Create related CapOrder objects
        cap_orders = [
            CapOrder(
                order=order,
                cap=item.get("cap"),
                price=item.get("cap").price,
                quantity=item.get("quantity"),
            )
            for item in cart.items
        ]
        CapOrder.objects.bulk_create(cap_orders)

        order.payment = Payment.objects.create(
            customer=user,
            amount=sum(cap_order.total_price for cap_order in cap_orders),
        )

        order.save(update_fields=["payment"])

        # 4. Clear the cart
        cart.clear()

        return order