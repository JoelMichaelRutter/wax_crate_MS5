from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_cart, name='show_cart'),
    path('add/<record_id>/', views.add_record_to_cart, name='add_record_to_cart'),
]