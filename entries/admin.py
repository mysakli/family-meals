from django.contrib import admin
from .models import Meal, MealType


# Register your models here.
admin.site.register([Meal, MealType])