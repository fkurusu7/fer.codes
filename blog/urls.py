from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts, name='posts'),
    path('post/<int:post_id>', views.post_detail, name='post'),
    path('post/add_post', views.add_post, name='add_post'),
    path('post/edit/<int:post_id>', views.edit_post, name='edit_post'),
]
