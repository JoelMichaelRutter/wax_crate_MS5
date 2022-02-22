from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Record, Genre


def all_records(request):
    """
    This view shows all the records in the shop.
    This view also handles search queries and filtering.
    """
    records = Record.objects.all()
    genres = Genre.objects.all()
    query = None
    genre = None
    sort = None
    direction = None
    # Checks if there is a get request in user request.
    # If get request exsists, assign name of search
    # form to query variable.

    if request.GET:

        if 'sort' in request.GET:
            sorting_key = request.GET['sort']
            sort = sorting_key
            if sorting_key == 'title':
                sorting_key = 'title_lower'
                records = records.annotate(title_lower=Lower('title'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sorting_key = f'-{sorting_key}'
            records = records.order_by(sorting_key)

        # This code block handles the filtering by genre functionality.
        if 'genre' in request.GET:
            genre = request.GET['genre']
            records = records.filter(genre__genre__contains=genre)
            genres = Genre.objects.filter(genre__contains=genre)
        # This code block handles the filtering by hot pick functionality.
        elif 'hot_picks' in request.GET:
            records = records.filter(hot_pick=True)

        # This code block handles the search form queries.
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter anything into the search bar!"
                    )
                return redirect(reverse('records'))

            queries = (Q(title__icontains=query) |
                       Q(artist__icontains=query) |
                       Q(record_label__icontains=query))
            records = records.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'records': records,
        'search_term': query,
        'current_genre': genres,
        'current_sorting': current_sorting,
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
