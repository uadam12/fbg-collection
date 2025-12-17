from django.urls import path
from . import views


app_name = 'payment'


urlpatterns = [
    path('', views.payments_list, name='list'),
    path('<int:pk>/', views.payment_detail, name='detail'),
    path('<int:order_id>/verify/', views.verify_payment, name='verify')
]