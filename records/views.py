"""
1 - Importing login required decorator to secure CRUD functionality.
2 - Importing render, GOO404, redirect and reverse shortcuts for us in views.
3 - Importing messages framework
4 - Importing Q for database querying within all records view.
5 - Importing lower function for use in all records view.
6 - Importing Record and Genre models for accessing db entries.
7 - Importing record form from forms.py to add to context.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Record, Genre
from .forms import RecordForm, GenreForm


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
        # Thiw code block hanldes the sorting functionality
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


@login_required()
def load_back_office(request):
    """
    A view to load the back office template
    and relevant forms. The post handlers for
    these forms are in different views.
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            f"Sorry, {request.user}, you aren't an admin \
            so you cant access this area."
        )
        return redirect(reverse('home'))
    else:
        add_record_form = RecordForm()
        add_genre_form = GenreForm()

        template = 'records/back_office.html'
        context = {
            'add_record_form': add_record_form,
            'add_genre_form': add_genre_form,
        }

        return render(request, template, context)


@login_required
def add_record(request):
    """
    This view takes the data submitted by
    the record form in the back office.
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            f"Sorry, {request.user}, you aren't an admin \
            so you cant access this area."
        )
        return redirect(reverse('home'))
    if request.method == 'POST':
        add_record_form = RecordForm(request.POST, request.FILES)
        try:
            if add_record_form.is_valid():
                add_record_form.save()
                messages.success(
                    request,
                    "Record added succesfully"
                )
                return redirect(reverse('records'))
            else:
                messages.error(
                    request,
                    f'{add_record_form.errors}'
                )
                return redirect(reverse('add_record'))
        except IntegrityError as error:
            messages.error(
                request,
                f'The record you are trying to add already exists \
                    {error}'
            )
            return redirect(reverse('back_office'))


@login_required
def add_genre(request):
    """
    This view takes the data submitted by
    the genre form in the back office.
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            f"Sorry, {request.user}, you aren't an admin \
            so you cant access this area."
        )
        return redirect(reverse('home'))
    if request.method == 'POST':
        add_genre_form = GenreForm(request.POST)
        try:
            if add_genre_form.is_valid():
                add_genre_form.save()
                messages.success(
                    request,
                    "Genre added succesfully"
                )
                return redirect(reverse('back_office'))
            else:
                messages.error(
                    request,
                    f'{add_genre_form.errors}'
                )
                return redirect(reverse('back_office'))
        except IntegrityError as error:
            messages.error(
                request,
                f'The genre you are trying to add already exists \
                    {error}'
            )
            return redirect(reverse('back_office'))


@login_required
def edit_record(request, record_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(
            request,
            f"Sorry, {request.user}, you aren't an admin \
            so you cant access this area."
        )
        return redirect(reverse('home'))

    record = get_object_or_404(Record, pk=record_id)
    if request.method == 'POST':
        edit_record_form = RecordForm(request.POST, request.FILES, instance=record)
        if edit_form.is_valid():
            edit_record_form.save()
            messages.success(request, 'Record updated successfully')
            return redirect(reverse('records'))
        else:
            messages.error(
                request,
                'Looks like some funky values in your data, please check them and try again.'
            )
    else:
        edit_record_form = RecordForm(instance=record)
        messages.info(request, f'You are editing {record.title}')

    template = 'records/edit_record.html'
    context = {
        'edit_record_form': edit_record_form,
        'record': record,
    }

    return render(request, template, context)


@login_required
def delete_record(request, record_id):
    """
    View to remove records from the database
    This is triggered via a modal on the records
    page.
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            f"Sorry, {request.user}, you aren't an admin \
            so you cant access this area."
        )
        return redirect(reverse('home'))
    record = get_object_or_404(Record, pk=record_id)
    record.delete()
    messages.success(
        request,
        "Record deleted successfully."
    )
    return redirect(reverse('records'))


@login_required
def delete_genre(request, genre_id):
    """
    View to remove genres from the database
    This is triggered via a modal on the back office
    page.
    """
    if not request.user.is_superuser:
        messages.error(
            request,
            f"Sorry, {request.user}, you aren't an admin \
            so you cant access this area."
        )
        return redirect(reverse('home'))
    genre = get_object_or_404(Genre, pk=genre_id)
    genre.delete()
    messages.success(
        request,
        "Genre deleted successfully."
    )
    return redirect(reverse('back_office'))
