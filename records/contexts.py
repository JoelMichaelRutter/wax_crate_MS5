"""
Importing genre model to find genres.
"""
from .models import Genre


def genres_in_database(request):
    """
    This function gets all of the objects stored
    in the Genre model table and through the
    TEMPLATE context processer setting, allows
    the entries to be utilised across the entire
    site. Namely, in the dropdown navigation so
    that an option can be rendered for each genre.
    """
    genres = Genre.objects.all()

    context = {
        'genres': genres,
    }

    return context
