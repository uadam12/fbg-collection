from django.db import models, transaction
from payment.models import Payment
from user.models import User
from cap.models import Cap


class Order(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_SHIPPING = "shipping"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELED = "canceled"
    STATUS_REFUNDED = "refunded"
    STATUS_RETURNED = "returned"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_SHIPPING, "Shipping"),
        (STATUS_DELIVERED, "Delivered"),
        (STATUS_CANCELED, "Canceled"),
        (STATUS_REFUNDED, "Refunded"),
        (STATUS_RETURNED, "Returned"),
    )

    payment = models.OneToOneField(
        Payment, 
        on_delete=models.SET_NULL, 
        related_name='order',
        null=True, blank=True,
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    caps = models.ManyToManyField(
        Cap,
        through="CapOrder",
        related_name="orders"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    shipping_address = models.TextField()
    ordered_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(cap_order.total_price for cap_order in self.cap_orders.all())

    class Meta:
        ordering = ["-ordered_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.pk} ({self.get_status_display()})"


class CapOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="cap_orders")
    cap = models.ForeignKey(Cap, on_delete=models.CASCADE, related_name="cap_orders")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} × {self.cap.name} for Order #{self.order.pk}"
