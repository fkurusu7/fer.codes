# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Python
from collections import defaultdict

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
    categories = Category.objects.all()
    context = { 'post': post, 'categories': categories }
    return render(request, 'blog/post_detail.html', context)

def editor_test(request):
    print(request.POST)
    
def add_post(request):
    print(request.POST)
    if request.method == 'POST':
        # Get form values
        title = request.POST['title']

        summary = request.POST['summary']

        if not request.POST.get('status'):
            status = 'draft'
        else:
            status = request.POST['status']

        content = request.POST['content']

        # Categories
        categories = _get_categories(request) 

        # Thumbnail Photo
        if not request.FILES.get('thumbnail'):
            thumbnail = ""
        else:
            thumbnail = request.FILES['thumbnail']
       
        errors = ''
        if Post.objects.filter(title=title).exists():
            errors += '\nTitle is taken, pick another one.'
        if not content:
            errors += '\nPost Content must not be empty'
        if not summary:
            errors += '\nSummary must not be empty'

        if not errors:
            post = Post(title= title, content= content, summary= summary, status= status, thumbnail=thumbnail)
            post.save()
            post.categories.add(*categories)

            messages.success(request, 'Post added.')
            return redirect('posts')

        else:
            messages.error(request, errors)
            return redirect('add_post')
    else:
        categories = Category.objects.all()
        context = { 'categories': categories }
        return render(request, 'blog/add_post.html', context)

  
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

    # Categories from TEXTBOXES (commas)
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
