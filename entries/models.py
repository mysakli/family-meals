from django.db import models
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import django_filters




# Create your models here.

class MealType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    

class Meal(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='uploads/', blank=True, null=True)
    recipe = models.URLField(max_length=500, blank=True, null=True, help_text='Enter a valid URL, e.g., https://example.com')
    date_created = models.DateTimeField(default=timezone.now)
    vegetarian = models.BooleanField(default=False)
    meal_type = models.ForeignKey(MealType, on_delete=models.PROTECT)
    grandma = models.BooleanField(default=False)
    notes = models.TextField(max_length=500, blank=True,  verbose_name='Notes',
    help_text='e.g. recipe notes.')


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Only process the photo if it's a new upload
        if self.photo and hasattr(self.photo, 'file'):
            try:
                # Read file into memory before processing (needed for S3)
                self.photo.file.seek(0)
                img = Image.open(self.photo.file)
                img = img.convert('RGB')  # Convert to RGB (removes alpha transparency)
                
                # Calculate target dimensions while maintaining aspect ratio
                target_size = 200
                ratio = max(target_size / img.size[0], target_size / img.size[1])
                new_size = tuple([int(x * ratio) for x in img.size])
                
                # Resize image maintaining aspect ratio
                img = img.resize(new_size, Image.LANCZOS)
                
                # Calculate cropping coordinates to center the image
                left = (new_size[0] - target_size) // 2
                top = (new_size[1] - target_size) // 2
                right = left + target_size
                bottom = top + target_size
                
                # Crop to square
                img = img.crop((left, top, right, bottom))
                
                # Save the processed image to buffer
                buffer = BytesIO()
                img.save(buffer, format='JPEG', quality=85)
                buffer.seek(0)
                
                # Replace the photo field with processed image
                file_name = self.photo.name
                self.photo.save(file_name, ContentFile(buffer.getvalue()), save=False)
                
            except Exception as e:
                import traceback
                traceback.print_exc()

        super(Meal, self).save(*args, **kwargs)
    
    def get_photo_url(self):
        if self.photo:
            return {'url': self.photo.url, 'alt_text': self.name}
        # Use default storage to build the correct URL for both local and S3
        from django.core.files.storage import default_storage
        default_photo_path = 'img-null.jpg'
        if default_storage.exists(default_photo_path):
            default_url = default_storage.url(default_photo_path)
        else:
            # Fallback if file doesn't exist
            default_url = f'{settings.MEDIA_URL}{default_photo_path}'
        return {'url': default_url, 'alt_text': 'No photo'} 
    




