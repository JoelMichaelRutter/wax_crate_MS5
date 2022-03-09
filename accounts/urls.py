from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_customer_account, name='your_account'),
    path(
        'order_details/<order_number>/',
        views.order_details,
        name='order_details'
    ),
]
