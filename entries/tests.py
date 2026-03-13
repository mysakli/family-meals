import tempfile
import shutil
from io import BytesIO
from PIL import Image
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from .models import Meal, MealType

# Create a temporary directory for media files during tests
MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ModelTests(TestCase):
    def setUp(self):
        self.meal_type = MealType.objects.create(name="Dinner")

    def tearDown(self):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def test_meal_type_str(self):
        self.assertEqual(str(self.meal_type), "Dinner")

    def test_meal_str(self):
        meal = Meal.objects.create(
            name="Pizza",
            meal_type=self.meal_type
        )
        self.assertEqual(str(meal), "Pizza")

    def test_meal_image_processing(self):
        # Create a dummy image
        file_obj = BytesIO()
        image = Image.new("RGB", (400, 300), color="red")
        image.save(file_obj, "jpeg")
        file_obj.seek(0)
        
        photo = SimpleUploadedFile("test_image.jpg", file_obj.read(), content_type="image/jpeg")
        
        meal = Meal.objects.create(
            name="Resized Meal",
            meal_type=self.meal_type,
            photo=photo
        )
        
        # Verify image was resized to 200x200 (as per models.py)
        # Note: Meal.save() calls self.photo.save(..., save=False) then super().save()
        # We use .file instead of .path because some backends (like S3) don't support absolute paths
        img = Image.open(meal.photo.file)
        self.assertEqual(img.size, (200, 200))

    def test_get_photo_url_with_photo(self):
        file_obj = BytesIO()
        image = Image.new("RGB", (100, 100), color="blue")
        image.save(file_obj, "jpeg")
        file_obj.seek(0)
        photo = SimpleUploadedFile("test.jpg", file_obj.read(), content_type="image/jpeg")
        
        meal = Meal.objects.create(name="Test Meal", meal_type=self.meal_type, photo=photo)
        photo_info = meal.get_photo_url()
        # Use uploads/test instead of test.jpg because Django might append random strings
        self.assertIn("uploads/test", photo_info['url'])
        self.assertEqual(photo_info['alt_text'], "Test Meal")

    def test_get_photo_url_without_photo(self):
        meal = Meal.objects.create(name="No Photo Meal", meal_type=self.meal_type)
        photo_info = meal.get_photo_url()
        self.assertIn("img-null.jpg", photo_info['url'])
        self.assertEqual(photo_info['alt_text'], "No photo")

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.meal_type = MealType.objects.create(name="Lunch")
        self.meal = Meal.objects.create(
            name="Salad",
            meal_type=self.meal_type,
            vegetarian=True
        )

    def test_meal_list_view(self):
        response = self.client.get(reverse('meal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Salad")
        self.assertIn('meals', response.context)

    def test_meal_detail_view(self):
        response = self.client.get(reverse('meal-detail', kwargs={'pk': self.meal.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Salad")

    def test_meal_create_view(self):
        from django.utils import timezone
        response = self.client.post(reverse('meal-create'), {
            'name': 'New Meal',
            'meal_type': self.meal_type.pk,
            'vegetarian': False,
            'grandma': False,
            'notes': 'Some notes',
            'date_created': timezone.now()
        })
        if response.status_code != 302:
             print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302) # Redirect to list
        self.assertTrue(Meal.objects.filter(name='New Meal').exists())

    def test_meal_update_view(self):
        from django.utils import timezone
        response = self.client.post(reverse('meal-update', kwargs={'pk': self.meal.pk}), {
            'name': 'Updated Salad',
            'meal_type': self.meal_type.pk,
            'vegetarian': True,
            'grandma': False,
            'notes': 'Updated notes',
            'date_created': timezone.now()
        })
        if response.status_code != 302:
             print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.meal.refresh_from_db()
        self.assertEqual(self.meal.name, "Updated Salad")

    def test_meal_delete_view(self):
        response = self.client.post(reverse('meal-delete', kwargs={'pk': self.meal.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Meal.objects.filter(pk=self.meal.pk).exists())

class FilterTests(TestCase):
    def setUp(self):
        self.dinner = MealType.objects.create(name="Dinner")
        self.lunch = MealType.objects.create(name="Lunch")
        Meal.objects.create(name="Beef Stew", meal_type=self.dinner, vegetarian=False)
        Meal.objects.create(name="Veggie Pasta", meal_type=self.dinner, vegetarian=True)
        Meal.objects.create(name="Cheese Sandwich", meal_type=self.lunch, vegetarian=True)

    def test_filter_by_vegetarian(self):
        response = self.client.get(reverse('meal-list'), {'vegetarian': 'True'})
        self.assertEqual(len(response.context['meals']), 2)
        self.assertContains(response, "Veggie Pasta")
        self.assertContains(response, "Cheese Sandwich")
        self.assertNotContains(response, "Beef Stew")

    def test_filter_by_meal_type(self):
        response = self.client.get(reverse('meal-list'), {'meal_type': self.lunch.pk})
        self.assertEqual(len(response.context['meals']), 1)
        self.assertContains(response, "Cheese Sandwich")

    def test_filter_by_name(self):
        response = self.client.get(reverse('meal-list'), {'name': 'stew'})
        self.assertEqual(len(response.context['meals']), 1)
        self.assertContains(response, "Beef Stew")
