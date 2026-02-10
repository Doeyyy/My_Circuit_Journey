from django.db import models
# from django.contrib.auth import User
from django.utils.text import slugify
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Categories(models.Model):
    title = models.CharField(max_length = 150)
    slug = models.SlugField(unique= True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args,**kwargs)
    def __str__(self):
        return self.title
    
    
from django.urls import reverse
class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    title =models.CharField(max_length=100, unique=True, blank = True, null = False)
    slug = models.SlugField(unique=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)  # local or S3
   # Store the Backblaze file path and URL directly
    video= models.FileField(upload_to= 'videos/', blank=True, null=True)
    # video_name = models.CharField(max_length=200, blank=True, null=True) 
    
    body = CKEditor5Field('Text', config_name='extends')
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Categories', on_delete=models.SET_NULL, null=True, blank=True, related_name="blogs")
    

    
    def __str__(self):
        return self.title

    
    
class Comments(models.Model):
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, models.CASCADE)
    
    def __str__(self):
        return self.body