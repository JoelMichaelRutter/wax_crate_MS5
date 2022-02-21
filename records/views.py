from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Record


def all_records(request):
    """
    This view shows all the records in the shop.
    """
    records = Record.objects.all()
    query = None
    # Checks if there is a get request in user request.
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "Sorry, we dont stock that at the moment"
                    )
                return redirect(reverse('records'))

            queries = (Q(title__icontains=query) |
                       Q(artist__icontains=query) |
                       Q(record_label__icontains=query))

            records = records.filter(queries)

    context = {
        'records': records,
        'search_term': query,
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
