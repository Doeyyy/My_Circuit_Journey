from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from Circuit_Journey.models import Blog

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully")
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()  #  Correctly placed here
    context = {'form': form}
    return render(request, 'core/signup.html', context)


def signin(request):
    if request.method == "POST":
        # Get username or email from form
        username_or_email = request.POST.get("username_or_email")
        password = request.POST.get("password")
        
        # First try to authenticate with email
        user = authenticate(request, email=username_or_email, password=password)
        
        # If that fails, try with username
        if user is None:
            user = authenticate(request, username=username_or_email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid email/username or password")
            return redirect('signin')
    
    return render(request, 'core/signin.html')

def signout(request):
    logout(request)  
    return redirect('index')

def profile(request):
    user = request.user
    blogs = Blog.objects.filter(user= user)
    context = {'user': user, "blogs":blogs}
    return render(request, 'core/profile.html', context)


@login_required(login_url="signin")
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            # to Return updated profile display (not redirect)
            return render(request, 'core/partials/profile_info.html', {"user": user})

    else:
        form = UpdateProfileForm(instance=user)

    return render(request, 'core/partials/edit_profile_form.html', {"form": form})

