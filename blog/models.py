from django.db import models
from django.db import IntegrityError 
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) :
        return self.name
        
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    img_url = models.FileField(null=True, upload_to="posts/images")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_published = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
        
    def __str__(self) :
        return self.title