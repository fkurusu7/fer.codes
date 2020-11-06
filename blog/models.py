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
    description = models.TextField()
    summary = models.CharField(max_length=300)
    publish_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default='draft', choices=STATUS_CHOICES)
    main_photo = models.ImageField(upload_to='blog/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True)


    def __str__(self):
        return self.title


    class Meta:
        ordering = ('-publish_date',)
