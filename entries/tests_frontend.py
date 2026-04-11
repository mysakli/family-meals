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
        self.assertContains(response, 'grid-cols-2')
        self.assertContains(response, 'md:grid-cols-4')
        self.assertContains(response, 'rounded-xl')

    def test_meal_list_has_touch_friendly_links(self):
        """Verify that edit and delete links have classes that can be styled for touch targets."""
        response = self.client.get(reverse('meal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'text-primary')
        self.assertContains(response, 'text-red-600')

    def test_meal_form_uses_tailwind_classes(self):
        """Verify that the meal form uses Tailwind styling."""
        response = self.client.get(reverse('meal-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rounded-xl')
        self.assertContains(response, 'bg-primary')
        self.assertContains(response, 'text-slate-600')

    def test_meal_form_checkboxes_use_tailwind_sizing_classes(self):
        """Verify that checkbox inputs override the global input height with Tailwind classes."""
        response = self.client.get(reverse('meal-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="h-5 w-5 rounded border-slate-300')

    def test_meal_form_renders_meal_type_as_select(self):
        """Verify that the meal_type field renders as a select instead of a text input."""
        response = self.client.get(reverse('meal-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="meal_type"')
        self.assertContains(response, 'id="id_meal_type"')
        self.assertContains(response, 'rounded-xl')
        self.assertContains(response, 'border-slate-300')
        self.assertContains(response, f'<option value="{self.meal_type.pk}">{self.meal_type.name}</option>', html=True)

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

    def test_meal_detail_uses_tailwind_classes(self):
        """Verify that the meal detail view uses Tailwind styling."""
        response = self.client.get(reverse('meal-detail', kwargs={'pk': self.meal.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rounded-xl')
        self.assertContains(response, 'bg-amber-500')
        self.assertContains(response, 'bg-red-600')

