from django.urls import path
from order import views

app_name = 'order'


urlpatterns = [
    path('', views.orders, name='list'),
    path('<int:pk>/', views.order, name='detail'),
    path('<int:pk>/update/', views.update_order, name='update'),
]