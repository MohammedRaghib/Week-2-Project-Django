from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistration
from .models import Photo, Profile, Tag
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        print(bool(user))
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home_tagless')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'login.html')

def register_view(request):
    form = UserRegistration()
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home_tagless')
        else:
            messages.error(request, 'Please correct the error below.')
    
    return render(request, 'register.html', {'form': form})

@login_required
def home(request, tagname=None): 
    tags = Tag.objects.all()
    if tagname: 
        tags = Tag.objects.filter(name=tagname)
        photos = Photo.objects.filter(tags__in=tags) 
    else: 
        photos = Photo.objects.all() 
    return render(request, 'base.html', {'photos': photos, 'tags': tags})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    prof = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        profpicture = request.POST.get('profpic')
        username = request.POST.get('username', user.username)
        first_name = request.POST.get('first_name', user.first_name)
        last_name = request.POST.get('last_name', user.last_name)
        email = request.POST.get('email', user.email)

        if profpicture:
             prof.image.url = profpicture
        user.username = username 
        user.first_name = first_name 
        user.last_name = last_name 
        user.email = email 
        user.save()
        prof.save() 
        messages.success(request, 'Profile updated successfully!') 
        return redirect('profile')
    return render(request, 'profile.html', {'prof': prof})

@login_required
def like(request, picid):
    photo = get_object_or_404(Photo, id=picid)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        if request.user in photo.dislikes.all():
            photo.dislikes.remove(request.user)
        photo.likes.add(request.user)
    return redirect('home_tagless')

@login_required
def dislike(request, picid):
    photo = get_object_or_404(Photo, id=picid)
    if request.user in photo.dislikes.all():
        photo.dislikes.remove(request.user)
    else:
        if request.user in photo.likes.all():
            photo.likes.remove(request.user)
        photo.dislikes.add(request.user)
    return redirect('home_tagless')

def editprof(request):
    return render(request, 'editprof.html')
def custom_404(request, exception): 
    return render(request, '404.html', status=404)