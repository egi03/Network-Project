import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow, Like


def paginate_and_serialize(posts, page_number="1"):
    # Paginate the posts (10 per page)
    
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)

    serialized_posts = serialize('json', page_obj)
    return serialized_posts

def get_page_object(posts, page_number):
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)

    return page_obj

def index(request):
    all_posts = Post.objects.all().order_by('-date')
    page_number = request.GET.get('page', 1)
    
    page_obj = get_page_object(all_posts, page_number)
    serialized_posts = paginate_and_serialize(all_posts, page_number)
    return render(request, "network/index.html", {
        "posts_json": serialized_posts,
        "likes_json": serialize('json', Like.objects.all()),
        "users_json": serialize('json', User.objects.all()),
        "page_obj": page_obj,
        "current_user": request.user.username
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def create_post(request):
    if request.method == "POST":
        user = request.user
        text = request.POST["text"]
        post = Post(user=user, content=text)
        post.save()
    
    return HttpResponseRedirect(reverse("index"))

def show_profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by('date')
    number_of_followers = Follow.objects.filter(subject=user).count()
    number_of_following = Follow.objects.filter(follower = user).count()
    if(request.user.is_authenticated):
        is_viewing_his_page = user == request.user
        is_following = Follow.objects.filter(follower=request.user, subject=user).exists()
    else:
        is_viewing_his_page = True
        is_following = False
    page_number = request.GET.get('page', 1)
    serialized_json_posts = paginate_and_serialize(posts, page_number)
    page_obj = get_page_object(posts, page_number)
    
    return render(request, "network/profile.html", {
        "user": user,
        "is_viewing_his_page": is_viewing_his_page,
        "is_following": is_following,
        "number_of_followers": number_of_followers,
        "number_of_following": number_of_following,
        "posts_json": serialized_json_posts,
        "likes_json": serialize('json',Like.objects.all()),
        "page_obj": page_obj,
        "current_user": request.user.username,
        "users_json":  serialize('json',User.objects.all()),
    })
    
def toggle_follow(request):
    profile_username = request.POST.get('profileUser')
    profile_user = User.objects.get(username=profile_username)
    is_following = Follow.objects.filter(follower=request.user, subject=profile_user).exists()
    if(is_following):
        Follow.objects.filter(follower=request.user, subject=profile_user).delete()
    else:
        newFollow = Follow.objects.create(follower=request.user, subject=User.objects.get(username=profile_user))
        newFollow.save()
    
    return HttpResponseRedirect(reverse("show_profile", args=[profile_user]))

def following_view(request):
    posts = Post.objects.all()
    following_posts = Post.objects.none()
    following = Follow.objects.filter(follower=request.user)
    for post in posts:
        for follow in following:
            if post.user == follow.subject:
                following_posts |= Post.objects.filter(pk=post.pk)
                
    page_number = request.GET.get('page', 1)
    
    page_obj = get_page_object(following_posts, page_number)
    serialized_posts = paginate_and_serialize(following_posts, page_number)
    
    return render(request, "network/following.html", {
        "posts_json": serialized_posts,
        "likes_json": serialize('json',Like.objects.all()),
        "users_json": serialize('json',User.objects.all()),
        "page_obj": page_obj,
        "current_user": request.user.username
    })
    

@csrf_exempt
def edit_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id', "")
        new_text = data.get('newText', "")
        
        post = Post.objects.filter(pk=id)
        post.update(content=new_text)
        post.save()
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        is_liked = data.get('isLiked', "")
        post_id =  data.get("id", "")
        userPk = data.get("user", "")
        
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(pk=userPk)
        
        if(not is_liked):
            like = Like.objects.create(post=post, user=user)
            like.save()
        else:
            Like.objects.filter(post=post_id, user=userPk).delete()

    
    return JsonResponse({"message": "Post updated successfully."}, status=201)
