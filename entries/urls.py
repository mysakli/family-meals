from django.urls import path
from . import views

urlpatterns = [
    path('', views.MealListView.as_view(), name='meal-list'),
    path('meal/<int:pk>', views.MealDetailView.as_view(), name='meal-detail'),
    path('create/', views.MealCreateView.as_view(),name='meal-create'),
    path('meal/<int:pk>/update', views.MealUpdateView.as_view(), name='meal-update',),
    path('meal/<int:pk>/delete', views.MealDeleteView.as_view(), name='meal-delete'),
]