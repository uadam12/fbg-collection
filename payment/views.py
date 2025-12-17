from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages

from app.decorators import staff_required
from payment.models import Payment
from order.models import Order


@staff_required
def payments_list(request: HttpRequest):
    """
    List all payments for staff users.
    """
    payments = Payment.objects.select_related("customer").all()

    return render(request, "payments/list.html", {
        "payments": payments,
        "statuses": Payment.STATUS_CHOICES,
    })


@staff_required
def payment_detail(request: HttpRequest, pk: int):
    """
    Display payment details for a single payment.
    """
    payment = get_object_or_404(Payment, pk=pk)

    return render(request, "payments/detail.html", {
        "payment": payment,
    })

@staff_required
def verify_payment(request: HttpRequest, order_id: int):
    """
    Verify a payment via Paystack and update its status.
    """
    order = get_object_or_404(
        Order.objects.select_related('payment'),
        pk = order_id
    )
    payment = order.payment

    if payment.verified:
        messages.info(request, "Payment already verified.")
    else:
        verified = payment.verify(request.GET.get("trxref", ''))

        if verified:
            order.status = Order.STATUS_PROCESSING
            order.save(update_fields=['status'])
            messages.success(request, f"Payment verified successfully.")
        else:
            messages.error(request, f"Payment your verification failed.")

    return redirect(reverse("payment:detail", kwargs={"pk": order.payment.pk}))
