from django.shortcuts import render
from .models import Record


def all_records(request):
    """
    This view shows all the records in the shop.
    """
    records = Record.objects.all()
    context = {
        'records': records,
    }
    return render(request, 'records/records.html', context)
