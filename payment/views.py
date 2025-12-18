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
    payments = Payment.objects.select_related("customer", "order")
    status = request.GET.get('status')

    if status:
        payments = payments.filter(status=status)

    return render(request, "payments/list.html", {
        "payments": payments,
        "statuses": Payment.STATUS_CHOICES,
    })


@login_required
def payment_detail(request: HttpRequest, pk: int):
    """
    Display payment details for a single payment.
    """
    payment = get_object_or_404(
        Payment.objects.filter(customer=request.user) 
        if not request.user.is_staff else Payment, 
        pk=pk
    )

    return render(request, "payments/detail.html", {
        "payment": payment,
    })

@login_required
def verify_payment(request: HttpRequest, order_id: int):
    """
    Verify a payment via Paystack and update its status.
    """

    # Base queryset
    qs = Order.objects.select_related('payment')

    # Restrict to user's orders if not staff
    if not request.user.is_staff:
        qs = qs.filter(customer=request.user)

    # Get the order or 404
    order = get_object_or_404(qs, pk=order_id)
    payment = order.payment

    # If already verified, inform the user
    if payment.verified:
        messages.info(request, "This payment has already been verified.")
        return redirect(reverse("payment:detail", kwargs={"pk": payment.pk}))

    # Get transaction reference from query parameters
    trx_ref = request.GET.get("trxref")
    if not trx_ref:
        # No reference provided, render verification page
        return render(request, 'payments/verify.html', {"order": order})

    # Verify payment
    if payment.verify(trx_ref):
        order.status = Order.STATUS_PROCESSING
        order.save(update_fields=['status'])
        messages.success(request, "Payment verified successfully.")
    else:
        messages.error(request, "Payment verification failed. Please try again.")

    return redirect(reverse("payment:detail", kwargs={"pk": payment.pk}))
