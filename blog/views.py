# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils import timezone

# Models
from .models import Post, Category


def posts(request):
    posts = Post.objects.filter(status='published')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    paged_posts = paginator.get_page(page)

    # Categories
    categories = Category.objects.all()
    
    # Posts by month
    month_posts = {}
    for paged_post in paged_posts:
        month = paged_post.publish_date.strftime('%B')
        if not month in month_posts:
            month_posts[month] = []
            month_posts[month].append(paged_post)
        else:
            month_posts[month].append(paged_post)
    
    context = {'month_posts': month_posts, 'categories': categories }
    return render(request, 'blog/posts.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    categories = post.categories.all()
    context = { 'post': post, 'categories': categories }
    return render(request, 'blog/post_detail.html', context)
    

def add_post(request):
    if request.method == 'POST':
        errors, is_valid = _save_post_is_valid(request)
        if is_valid:
            _save_post(request)
            messages.success(request, ('Post edited.'))
            return redirect('posts')
        else:
            messages.error(request, errors)
            return redirect('add_post')
    else:
        categories = Category.objects.all()[:10]
        context = { 'categories': categories }
        return render(request, 'blog/add_post.html', context)


# Validates Title and Content are not blank, and Title not existing in DB
def _save_post_is_valid(request):
    errors = ''
    is_valid = True

    if not request.POST.get('title'):
        errors += '\nTitle cannot be blank. Please fix it.'
        is_valid = False
    if Post.objects.filter(title=request.POST.get('title')).exists():
        errors += '\nTitle is taken, pick another one.'
        is_valid = False
    if not request.POST.get('content'):
        errors += '\nPost Content must not be blank. Please write something interesting.'
        is_valid = False
    
    return errors, is_valid


def _save_post(request):
    # Get form values
    title = request.POST['title']
    content = request.POST['content']
    status = 'draft' if not request.POST.get('status') else request.POST['status']
    thumbnail = "" if not request.FILES.get('thumbnail') else request.FILES['thumbnail']
    categories = _get_categories(request) 
    post = Post(title= title, content= content, status= status, thumbnail= thumbnail)
    post.save()
    post.categories.add(*categories)
    

def _get_categories(request):
    # https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/
    # Categories from CHECKBOXES
    if not request.POST.get('category_checkbox'):
        categories_checkbox = []
    else:
        categories_checkbox = []
        categories = request.POST.getlist('category_checkbox')
        for category in categories:
            cat = Category.objects.get(name= category)
            categories_checkbox.append(cat)

    # Categories from TEXTBOX (commas)
    if not request.POST.get('categories_comma'):
        categories_comma = []
    else:
        categories_comma = []
        categories = request.POST['categories_comma'].split(',')
        for category in categories:
            cat, created = Category.objects.get_or_create(name= category.strip())
            categories_comma.append(cat)

    categories = categories_checkbox + categories_comma 
    return categories


def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    categories = Category.objects.all()
    context = { 'post': post, 'categories': categories }
    if request.method == 'POST':
        errors, is_valid = _update_post_is_valid(request)
        if is_valid:
            _update_post(request, post)
            messages.success(request, ('Post edited.'))
            return redirect('posts')
        else:
            print(errors)
            messages.error(request, (errors))
            return render(request, 'blog/edit_post.html', {})
    else:
        return render(request, 'blog/edit_post.html', context)


def _update_post_is_valid(request):
    errors = ''
    is_valid = True

    if not request.POST.get('title'):
        errors += '\nTitle cannot be blank. Please fix it.'
        is_valid = False
    if not request.POST.get('content'):
        errors += '\nPost Content must not be blank. Please write something... interesting.'
        is_valid = False
    
    return errors, is_valid


def _update_post(request, post):
    # Get form values
    title = request.POST['title']
    content = request.POST['content']
    status = 'draft' if not request.POST.get('status') else request.POST['status']
    publish_date = post.publish_date
    if status == 'published':
        publish_date = timezone.now()
    thumbnail = "" if not request.FILES.get('thumbnail') else request.FILES['thumbnail']
    categories = _get_categories(request)
    
    post.title = title
    post.content = content
    post.status = status
    post.thumbnail = thumbnail
    post.publish_date = publish_date
    post.save(force_update=True)
    
    post.categories.clear()
    post.categories.add(*categories)
    