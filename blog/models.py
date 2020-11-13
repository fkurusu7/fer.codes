from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    
    class Meta:
        ordering = ('-created', 'name',)


class Post(models.Model):
    # A Post can have multiple categories, and a category can be included in multiple Posts
    categories = models.ManyToManyField(Category)

    STATUS_CHOICES = (('draft', 'Draft'), ('published','Published'))

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique_for_date='publish_date') # Add to the slug the post author name
    content = models.TextField()
    summary = models.CharField(max_length=300)
    publish_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default='draft', choices=STATUS_CHOICES)
    thumbnail = models.ImageField(upload_to='blog/%Y/%m/%d/')

    def __str__(self):
        return self.title


    class Meta:
        ordering = ('-publish_date',)
