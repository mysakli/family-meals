import django_filters
from .models import Meal

class MealFilter(django_filters.FilterSet):
    BOOLEAN_CHOICES = (
        ('', 'All'),
        (True, 'Yes'),
        (False, 'No'),
    )
    grandma = django_filters.ChoiceFilter(choices=BOOLEAN_CHOICES)
    name = django_filters.CharFilter(lookup_expr='icontains')
    vegetarian = django_filters.ChoiceFilter(choices=BOOLEAN_CHOICES)

    class Meta:
        model = Meal
        fields = ['grandma', 'meal_type', 'name', 'vegeterian', ]