from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistration, PhotoForm
from .models import Photo, Profile, Tag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import re


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        print(bool(user))

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("home_tagless")
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("login")
    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#]).{8,}$"

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif not re.match(pattern, password1):
            messages.error(
                request,
                "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character.",
            )
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1,
                )
                user.save()
                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect("home_tagless")

    return render(request, "register.html")


@login_required
def home(request, tagname=None):
    tags = Tag.objects.all()
    if tagname:
        tags = Tag.objects.filter(name=tagname)
        photos = Photo.objects.filter(tags__in=tags)
    else:
        photos = Photo.objects.all()
    return render(request, "base.html", {"photos": photos, "tags": tags})

@login_required 
def upload_photo(request):
    photos = Photo.objects.all() 

    if request.method == 'POST':
        try:
            photo = request.POST['photo']
            description = request.POST['description']
            tag_names = request.POST.get('tags', '').strip() 
            tags = []

            if tag_names:
                for tag_name in tag_names.split(','):
                    tag_name = tag_name.strip()
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    tags.append(tag)

            new_photo = Photo.objects.create(
                photo=photo,
                description=description,
            )
            new_photo.tags.set(tags) 
            messages.success(request, 'Photo uploaded successfully!') 
            return redirect('home_tagless') 
        except Exception as e:
            messages.error(request, f'Error uploading photo: {e}') 

    return render(request, 'upload_photo.html', {'photos': photos}) 

def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    user = request.user
    prof = get_object_or_404(Profile, user=user)
    return render(request, "profile.html", {"prof": prof})


@login_required
def like(request, picid):
    photo = get_object_or_404(Photo, id=picid)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        if request.user in photo.dislikes.all():
            photo.dislikes.remove(request.user)
        photo.likes.add(request.user)
    return redirect("home_tagless")


@login_required
def dislike(request, picid):
    photo = get_object_or_404(Photo, id=picid)
    if request.user in photo.dislikes.all():
        photo.dislikes.remove(request.user)
    else:
        if request.user in photo.likes.all():
            photo.likes.remove(request.user)
        photo.dislikes.add(request.user)
    return redirect("home_tagless")


def editprof(request):
    user = request.user
    prof = get_object_or_404(Profile, user=user)
    if request.method == "POST":
        profpicture = request.POST.get("profpic")
        username = request.POST.get("username", user.username)
        first_name = request.POST.get("first_name", user.first_name)
        last_name = request.POST.get("last_name", user.last_name)
        email = request.POST.get("email", user.email)

        if profpicture:
            prof.photo = profpicture
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        prof.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")
    return render(request, "editprof.html")


def custom_404(request, exception):
    return render(request, "404.html", status=404)
