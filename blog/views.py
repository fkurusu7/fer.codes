from django.shortcuts import render

def blogs(request):
    return render(request, 'blog/blogs.html', {})
    
def blog(request, blog_id):
    return render(request, 'blog/blog.html', {})
