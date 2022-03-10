from django import forms
from .models import Genre, Record

# class GenreForm(forms.ModelForm):
#     class Meta:
#         model = Genre
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


class RecordForm(forms.ModelForm):
    """
    Class to render form from Record model.
    """
    class Meta:
        model = Record
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        genres = Genre.objects.all()

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'record-form-field'
