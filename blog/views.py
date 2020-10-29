from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Post


def posts(request):
    return render(request, 'blog/posts.html', {})


def post_detail(request, post_id):
    return render(request, 'blog/post_detail.html', {})


def add_post(request):
    if request.method == 'POST':
        # Get form values
        title = request.POST['title']
        summary = request.POST['summary']
        if not request.POST.get('status'):
            status = 'draft'
        else:
            status = request.POST['status']
        description = request.POST['description']
        main_photo = request.POST['main_photo']
        photo_1 = request.POST['photo_1']
        photo_2 = request.POST['photo_2']
        photo_3 = request.POST['photo_3']
        photo_4 = request.POST['photo_4']
        photo_5 = request.POST['photo_5']
        photo_6 = request.POST['photo_6']
        
        errors = ''
        if Post.objects.filter(title=title).exists():
            errors += '\nTitle is taken, pick another one.'
        if not description:
            errors += '\nDescription must not be empty'
        if not summary:
            errors += '\nSummary must not be empty'

        if not errors:
            post = Post(title= title, description= description, summary= summary, status= status, main_photo=main_photo, photo_1= photo_1, photo_2= photo_2, photo_3= photo_3, photo_4= photo_4, photo_5= photo_5, photo_6= photo_6)

            post.save()
            messages.success(request, 'Post added.')
            return redirect('posts')
        else:
            messages.error(request, errors)
            return redirect('add_post')
            
    else:
        return render(request, 'blog/add_post.html')

