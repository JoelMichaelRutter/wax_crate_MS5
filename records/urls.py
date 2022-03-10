
from django.urls import path
from . import views
# from .views import BackOffice

urlpatterns = [
    path('', views.all_records, name='records'),
    path('<slug>', views.show_record_details, name='show_record_details'),
    path('back_office/', views.back_office, name='back_office'),
    path('add/', views.add_record, name='add_record'),
]
