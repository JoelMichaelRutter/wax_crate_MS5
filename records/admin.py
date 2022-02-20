from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Genre, Record

# Register your models here.


class GenreAdmin(admin.ModelAdmin):
    """
    This admin class manages the genre model within
    the django admin.
    """
    list_display = [
        'genre'
    ]


class RecordAdmin(SummernoteModelAdmin):
    """
    This admin class manages the record model within
    the django admin.
    """
    list_display = [
        'id',
        'artist',
        'title',
        'record_label',
        'release_year',
        'hot_pick',
        'condition',
        'price',
        'has_link',
    ]

    ordering = ['title']

    prepopulated_fields = {'slug': ('title',)}

    summernote_fields = ('tracklist', 'description')


admin.site.register(Genre, GenreAdmin)
admin.site.register(Record, RecordAdmin)
