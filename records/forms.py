from django_summernote.widgets import SummernoteWidget
from django import forms
from .models import Genre, Record


class GenreForm(forms.ModelForm):
    """
    Form for adding genres via the genre model.
    """
    class Meta:
        """
        Meta class to describe which model.
        """
        model = Genre
        fields = ('genre',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['genre'].widget.attrs.update({'class': 'record-form-field'})


class RecordForm(forms.ModelForm):
    """
    Class to render form from Record model.
    """
    class Meta:
        """
        Meta class to confirm model and fields to render.
        """
        model = Record
        fields = (
            'genre',
            'image',
            'title',
            'artist',
            'record_label',
            'release_year',
            'hot_pick',
            'condition',
            'price',
            'tracklist',
            'description',
            'has_link',
            'link_to_music',
        )
        widgets = {
            'tracklist': SummernoteWidget(),
            'description': SummernoteWidget(),
        }

        labels = {
            'tracklist': 'Tracklist - UNORDERED LIST',
            'description': 'Description - BOLD KEY WORDS'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        genres = Genre.objects.all()

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'record-form-field'
