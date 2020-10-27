from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('<int:blog_id>', views.blog, name='blog'),
    path('add_blog', views.add_blog, name='add_blog'),
]
