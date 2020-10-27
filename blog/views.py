from django.shortcuts import render, redirect

def blogs(request):
    return render(request, 'blog/blogs.html', {})
    
def blog(request, blog_id):
    return render(request, 'blog/blog.html', {})

def add_blog(request):
    return render(request, 'blog/add_blog.html')
