from django.urls import path
from cart import views

app_name='cart'

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("order/", views.cart_order, name="order"),
    path("clear/", views.cart_clear, name="clear"),
    path("my-orders/", views.my_orders, name="my-orders"),
    path("my-orders/<order_id>/", views.my_order, name="my-order"),
    path("<int:cap_id>/toggle/", views.cart_toggle, name="toggle"),
    path("<int:cap_id>/remove/", views.cart_remove, name="remove"),
    path("<int:cap_id>/increase/", views.cart_increase, name="increase"),
    path("<int:cap_id>/decrease/", views.cart_decrease, name="decrease"),
]
