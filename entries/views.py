from django.shortcuts import render, redirect
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Meal, MealType
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

# Resize image before saving
def resize_image(image, size=(300, 300)):
    print(f'running resize_image fnc')
    img = Image.open(image).convert("RGB")  # Ensure RGB mode
    img.thumbnail(size, Image.LANCZOS)  # Maintain aspect ratio

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return ContentFile(buffer.getvalue())

def upload_meal(request):
    if request.method == "POST":
        meal = Meal(name=request.POST["name"])

        if "photo" in request.FILES:
            print(f'photo included')
            image = request.FILES["photo"]
            resized_image = resize_image(image)
            meal.photo.save(image.name, resized_image, save=True)
        else:
            print(f'photo not found')

        meal.save()
        print(f'new photo saved')
        return redirect("meal_list")  # Redirect after saving

    return render(request, "upload.html")

# Create your views here.

# class MealListView(FilterView, ListView):

class MealListView(FilterView):
    model = Meal
    queryset = Meal.objects.all().order_by('name')
    template_name = 'entries/meal_list.html'
    context_object_name = 'meals'
    filterset_class = None

    def get_filterset_class(self):
        from .filters import MealFilter
        return MealFilter
    
    

class MealDetailView(DetailView):
    model = Meal


class MealCreateView(CreateView):
    model = Meal
    fields = '__all__'
    success_url = reverse_lazy('meal-list')

class MealUpdateView(UpdateView):
    model = Meal
    fields = '__all__'
    
    def get_success_url(self):
        meal = self.get_object()
        return reverse_lazy('meal-detail', kwargs={'pk': meal.id})


class MealDeleteView(DeleteView):
    model = Meal
    success_url = reverse_lazy('meal-list')
