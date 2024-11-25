
# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,User
from django_extensions.db.fields import AutoSlugField


    
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name
    
    

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    thumbnail = models.ImageField(height_field=None, width_field=None, max_length=100)
    feature_image = models.ImageField(height_field=None, null=None, blank=None)
    discription = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



class User(AbstractUser):
   
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, blank=True)
    state = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(height_field=None, width_field=None, max_length=100)


    def __str__(self):
        return self.username
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name="replies", on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=250, default="User", null=True)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.text