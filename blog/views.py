from django.shortcuts import render, get_object_or_404
from .models import BlogPost, Comment
from .forms import ContactForm
from django.core.paginator import Paginator

def home(request):
    post_list = BlogPost.objects.all().order_by('-timestamp')
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/home.html', {'posts': posts})

def blogpost(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    comments = post.comments.all()
    if request.method == 'POST':
        name = request.POST['name']
        content = request.POST['content']
        Comment.objects.create(post=post, name=name, content=content)
    return render(request, 'blog/blogpost.html', {'post': post, 'comments': comments})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    form = ContactForm()
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            success = True
    return render(request, 'blog/contact.html', {'form': form, 'success': success})

def search(request):
    query = request.GET.get('q')
    results = BlogPost.objects.filter(title__icontains=query) if query else []
    return render(request, 'blog/search.html', {'results': results, 'query': query})
