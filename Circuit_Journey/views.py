from django.shortcuts import render, redirect, get_object_or_404
from django.http import response, request
from .models import *
from django.utils.text import slugify
from django.db.models import Q
from .forms import *
from django.contrib import messages
from django.views.decorators.http import require_http_methods #this will be foe the hx post merthod we will be using
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.core.exceptions import ValidationError

# Create your views here.
def  index(request):
    blogs = Blog.objects.all()
    featured_blog = Blog.objects.filter(featured = True).first()
    categories = Categories.objects.all()
    recent_posts= Blog.objects.order_by('created_at')[:3]
   

    context = {
        "blogs": blogs,
        "f_blog": featured_blog,
        "categories": categories,
        "recent_posts": recent_posts,
    }
    return render(request, "Circuit_Journey/index.html", context) 

def post_info(request, slug):
    blogs = Blog.objects.get(slug=slug)
    related_posts = Blog.objects.filter(category=blogs.category).exclude(id=blogs.id)[:4]
    comments = Comments.objects.all()
    comment = Commentform()
    if request.method =="POST":
        comment = Commentform(request.POST)
        if comment.is_valid():
            commented = comment.save(commit=False)
            commented.author = request.user
            commented.blog = blogs
            commented.save()
            return redirect('Post_info', slug = blogs.slug)
        
    context={'blogs':blogs, 'comments':comments, "related_posts": related_posts}
    return render(request, "Circuit_Journey/details.html", context)


def cat(request, slug):
    category_per_blog = get_object_or_404(Categories, slug=slug)
    categories = Categories.objects.all()
    blog_category = Blog.objects.filter(category=category_per_blog).order_by('created_at')[:3]
    recent_posts = Blog.objects.order_by('created_at')[:3]
    
    context = {
        "blogs": blog_category,
        "categories": categories,
        "recent_posts": recent_posts,
        "selected_category": category_per_blog,
    }
    return render(request, "Circuit_Journey/index.html", context)
    
def create_blog(request):
    form = Createblogform()
    if request.method == 'POST':
        form = Createblogform(request.POST, request.FILES)
        if form.is_valid():
            formed = form.save(commit=False)
            formed.category = Categories.objects.first()
            formed.slug= slugify(request.POST["title"])
            # formed.slug= slugify(formed.title)
        
            formed.user = request.user
            # Handle video upload
            formed.save()
            messages.success(request, "Article has been created successfully")
            return redirect('index')
    
    context = {'form': form}
    return render(request, "Circuit_Journey/create.html", context)

def edit_blog(request, slug):
    update = True
    blog = Blog.objects.filter(slug=slug)
    editform = Createblogform(instance=blog)
    if request.method == "POST": 
        editform= Createblogform(request.POST, request.FILES, instance=blog)
        if editform.is_valid():
            edit = editform.save(commit=False)
            edit.category = Categories.objects.first()
            edit.slug = slugify(edit.title)
            edit.user = request.user                    
            messages.success(request, "Article has been updated successfully")
            edit.save()
            return redirect('detail', slug=edit.slug)
        
    
    context = {"update": update, "form": editform, "object": blog}
    return render(request, "Circuit_Journey/create.html", context)
            



def search_blogs(request):
    query = request.GET.get('search', '').strip()
    blogs = Blog.objects.none()  # Start with empty queryset
    
    if query:  # Only search if there's a query
        blogs = Blog.objects.filter(
            Q(title__icontains=query) | 
            Q(body__icontains=query) |
            Q(category__title__icontains=query)
        ).distinct()[:10]  # Limit to 10 results and remove duplicates
    
    return render(request, 'Circuit_Journey/partials/search.html', {'blogs': blogs})


def delete_blog(request, slug):
    delete_article = True
    blog = Blog.objects.get(slug=slug) #reuqest for blog slug and check for the user
    blogs = Blog.objects.filter(user = request.user)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "deleted successfully")
        return redirect('profile')

    context = {"del":delete_article, "blog":blog, "blogs":blogs}
    return render(request, "core/profile.html", context)

from django.contrib.auth import get_user_model      
User = get_user_model()

def about(request):
    # assuming you only want YOUR profile shown
    # e.g., first superuser or a specific ID
    user = get_object_or_404(User, id=1)  # change ID to yours
    return render(request, "Circuit_Journey/about.html", {"user": user})

