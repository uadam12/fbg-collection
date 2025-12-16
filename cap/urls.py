from django.urls import path
from cap import views, cat_views

app_name='cap'

urlpatterns = [
    path('', views.caps, name='list'),
    path('create/', views.create_cap, name='create'),
    path('<int:pk>/edit/', views.update_cap, name='update'),
    path('<int:pk>/delete/', views.delete_cap, name='delete'),

    path('categories/', cat_views.categories, name='categories'),
    path('categories/create/', cat_views.create_category, name='create-category'),
    path('categories/<int:pk>/edit/', cat_views.update_category, name='update-category'),
    path('categories/<int:pk>/delete/', cat_views.delete_category, name='delete-category'),
]