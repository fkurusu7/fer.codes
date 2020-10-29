from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts, name='posts'),
    path('<int:post_id>', views.post_detail, name='blog'),
    path('add_post', views.add_post, name='add_post'),
]
