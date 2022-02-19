
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_records, name='records'),
    path('<slug>/', views.show_record_details, name='show_record_details'),
]