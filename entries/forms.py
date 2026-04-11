from django import forms
from django.utils import formats

from .models import Meal


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = '__all__'
        widgets = {
            'date_created': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_created'].input_formats = [
            '%Y-%m-%dT%H:%M',
            '%Y-%m-%dT%H:%M:%S',
            *formats.get_format('DATETIME_INPUT_FORMATS'),
        ]
