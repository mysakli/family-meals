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
        self.assertContains(response, '<nav class="bg-white border-b')
        self.assertContains(response, 'id="mobile-menu"')

    def test_base_layout_has_logo_icon(self):
        """Verify that the base layout includes the SVG logo icon."""
        response = self.client.get(reverse('meal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<svg class="h-8 w-8 text-slate-800')
        self.assertContains(response, '<svg')

    def test_meal_list_uses_card_layout_without_fixed_width(self):
        """Verify that the meal list uses Tailwind card styling."""
        response = self.client.get(reverse('meal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rounded-xl')
        self.assertContains(response, 'shadow-sm')

    def test_meal_list_has_touch_friendly_links(self):
        """Verify that edit and delete links have classes that can be styled for touch targets."""
        response = self.client.get(reverse('meal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'text-primary')
        self.assertContains(response, 'text-red-600')

    def test_meal_form_uses_bootstrap_classes(self):
        """Verify that the meal form uses Bootstrap 5 form-control classes."""
        response = self.client.get(reverse('meal-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="form-control')
        self.assertContains(response, 'class="btn btn-primary')
        self.assertContains(response, 'class="btn btn-secondary')

    def test_base_layout_has_tailwind_css(self):
        """Verify that the base layout includes the Tailwind CSS link tag."""
        response = self.client.get(reverse('meal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/static/css/tailwind.css"')

    def test_base_layout_has_tailwind_background_class(self):
        """Verify that the base layout includes the bg-background class on the body."""
        response = self.client.get(reverse('meal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<body class="bg-background">')

