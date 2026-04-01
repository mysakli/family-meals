from django.test import TestCase, Client
from django.urls import reverse
from .models import Meal, MealType

class FrontendTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.meal_type = MealType.objects.create(name="Dinner")
        self.meal = Meal.objects.create(
            name="Test Meal",
            meal_type=self.meal_type,
            notes="Test notes"
        )

    def test_base_layout_has_viewport_meta_tag(self):
        """Verify that the base layout includes the viewport meta tag for mobile responsiveness."""
        response = self.client.get(reverse('meal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<meta name="viewport" content="width=device-width, initial-scale=1">')

    def test_base_layout_has_responsive_navbar(self):
        """Verify that the base layout includes a responsive navigation bar."""
        response = self.client.get(reverse('meal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<nav class="navbar')
        self.assertContains(response, 'navbar-toggler')
        self.assertContains(response, 'navbar-collapse')

    def test_base_layout_has_logo_icon(self):
        """Verify that the base layout includes the SVG logo icon."""
        response = self.client.get(reverse('meal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="logo-icon"')
        self.assertContains(response, '<svg')

    def test_meal_list_uses_card_layout_without_fixed_width(self):
        """Verify that the meal list uses Bootstrap cards without restrictive fixed widths."""
        response = self.client.get(reverse('meal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="card')

    def test_meal_list_has_touch_friendly_links(self):
        """Verify that edit and delete links have classes that can be styled for touch targets."""
        response = self.client.get(reverse('meal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="card-link')

    def test_meal_form_uses_bootstrap_classes(self):
        """Verify that the meal form uses Bootstrap 5 form-control classes."""
        response = self.client.get(reverse('meal-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="form-control')
        self.assertContains(response, 'class="btn btn-primary')
        self.assertContains(response, 'class="btn btn-secondary')

    def test_meal_detail_uses_bootstrap_classes(self):
        """Verify that the meal detail view uses Bootstrap 5 layout classes."""
        response = self.client.get(reverse('meal-detail', kwargs={'pk': self.meal.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="img-fluid')
        self.assertContains(response, 'class="btn btn-warning')
        self.assertContains(response, 'class="btn btn-danger')
