from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .models import Post


def posts(request):
    posts = Post.objects.filter(status='published')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    paged_posts = paginator.get_page(page)
    context = {'posts': paged_posts}
    return render(request, 'blog/posts.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = { 'post': post}
    return render(request, 'blog/post_detail.html', context)


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

        main_photo = request.FILES['main_photo']

        if not request.FILES.get('photo_1'):
            photo_1 = ''
        else:
            photo_1 = request.FILES['photo_1']

        if not request.FILES.get('photo_2'):
            photo_2 = ''
        else:
            photo_2 = request.FILES['photo_2']

        if not request.FILES.get('photo_3'):
            photo_3 = ''
        else:
            photo_3 = request.FILES['photo_3']

        if not request.FILES.get('photo_4'):
            photo_4 = ''
        else:
            photo_4 = request.FILES['photo_4']

        if not request.FILES.get('photo_5'):
            photo_5 = ''
        else:
            photo_5 = request.FILES['photo_5']

        if not request.FILES.get('photo_6'):
            photo_6 = ''
        else:
            photo_6 = request.FILES['photo_6']
        
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

