from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_customer_account, name='your_account'),
]
