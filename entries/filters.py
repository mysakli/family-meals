import django_filters
from .models import Meal

class MealFilter(django_filters.FilterSet):
    BOOLEAN_CHOICES = (
        ('', 'All'),
        (True, 'Yes'),
        (False, 'No'),
    )
    grandma = django_filters.ChoiceFilter(choices=BOOLEAN_CHOICES)
    vegetarian = django_filters.ChoiceFilter(choices=BOOLEAN_CHOICES)
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Meal
        fields = ['meal_type', 'grandma', 'vegetarian', 'name']