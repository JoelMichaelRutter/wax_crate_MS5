"""
1 - Importing path (default)
2 - Importing views as dictionary
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_cart, name='show_cart'),
    path(
        'add/<record_id>/',
        views.add_record_to_cart,
        name='add_record_to_cart'
        ),
    path('amend/<record_id>/', views.amend_cart, name='amend_cart'),
    path(
        'remove/<record_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),
]
