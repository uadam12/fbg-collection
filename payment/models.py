from django.db import models
from payment.paystack import paystack
from user.models import User

class Payment(models.Model):
    """
    Model to represent a payment made by a user.
    Integrates with Paystack for payment initialization and verification.
    """

    # Payment status choices
    STATUS_PENDING = "pending"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAILED, "Failed"),
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="payments",
        help_text="The user who made the payment"
    )
    reference = models.CharField(
        max_length=100, unique=True,
        blank=True, editable=False,
        help_text="Unique payment reference"
    )
    amount = models.PositiveIntegerField(
        help_text="Amount in kobo (NGN minor units)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        help_text="Payment status"
    )
    checkout_url = models.URLField(
        blank=True, null=True, editable=False,
        help_text="URL for the user to complete the payment"
    )
    metadata = models.JSONField(
        blank=True, null=True,
        help_text="Optional additional data related to the payment"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def init_url(self, callback_url: str, metadata:dict={}) -> None:
        """
        Initialize the payment with Paystack and set the checkout URL.

        Args:
            callback_url (str): URL to redirect to after payment.
        """
        response = paystack.init_payment(
            email=self.customer.email,
            callback_url=callback_url,
            amount=self.amount,
            metadata=metadata
        )
        self.checkout_url = response.get("data", {}).get("authorization_url")
        self.save(update_fields=["checkout_url"])

    @property
    def verified(self) -> bool:
        return bool(str(self.reference).strip())

    def verify(self, reference: str) -> bool:
        """
        Verify the payment status with Paystack.

        Returns:
            bool: True if Paystack verification succeeded else False
        """
        result = paystack.verify_payment(reference)
        verified = result.get("status") and result["data"]["status"] == "success"

        if verified:
            self.reference = reference
            self.status = Payment.STATUS_SUCCESS
            self.save(update_fields=["status", "reference"])
        else:
            self.status = Payment.STATUS_FAILED
            self.save(update_fields=["status"])

        return self.verified

    def __str__(self) -> str:
        return f"{self.reference} - {self.status}"