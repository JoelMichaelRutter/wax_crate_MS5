from django.shortcuts import render, get_object_or_404
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


def show_record_details(request, slug):
    """
    This view shows the detail for the paticular record
    selected by the user. It takes the slug which is generated
    from the title of of the record and uses that to locate the
    correct database entry. It is then inseted as context into
    the record_details template and is also used within the URL.
    """
    record = get_object_or_404(Record, slug=slug)
    context = {
        'record': record,
    }
    return render(request, 'records/record_details.html', context)
