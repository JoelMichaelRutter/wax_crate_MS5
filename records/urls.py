"""
1 - Importing path (default)
2 - Importing app views as dictionary.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_records, name='records'),
    path('back_office/', views.load_back_office, name='back_office'),
    path('add_record/', views.add_record, name='add_record'),
    path('add_genre/', views.add_genre, name='add_genre'),
    path('edit/<int:record_id>/', views.edit_record, name='edit_record'),
    path(
        'delete_record/<int:record_id>/',
        views.delete_record,
        name='delete_record'
    ),
    path(
        'delete_genre/<int:genre_id>/',
        views.delete_genre,
        name='delete_genre'
    ),
    path('<slug>/', views.show_record_details, name='show_record_details'),
]
