
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_records, name='records'),
    path('back_office/', views.back_office, name='back_office'),
    path('add/', views.add_record, name='add_record'),
    path('edit/<int:record_id>/', views.edit_record, name='edit_record'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
    path('<slug>/', views.show_record_details, name='show_record_details'),
]
