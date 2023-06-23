from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import (
    User,
    Post,
)

import json

#########
# VIEWS #
#########

def index(request):
    return render(request, "network/index.html")


#######
# API #
#######

@csrf_exempt
def posts(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if not request.user.is_authenticated:
            return redirect(reverse("login"))

        elif data.get("content") is None:
            return JsonResponse({"error": "Post must have content."}, status=400)

        post = Post(
            author=request.user,
            content=data["content"]
        )
        post.save()
        return JsonResponse({"message": "Post created successfully."}, status=201)

    elif request.method == "GET":

        posts = Post.objects.all().order_by("-timestamp")

        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        number_of_pages = paginator.num_pages
        page_obj = paginator.get_page(page_number)

        response = {
            'num_pages': number_of_pages,
            'posts' : []
        }

        for post in page_obj:
            current_post = post.serialize()
            current_post["liked"] = post.likes.filter(id=request.user.id).exists()
            response["posts"].append(current_post)

        return JsonResponse(response, safe=False, status=200)

    elif request.method == "PUT":
        if not request.user.is_authenticated:
            return redirect(reverse("login"))

        data = json.loads(request.body)
        post = Post.objects.get(id=data["id"])

        if post.user != request.user:
            return JsonResponse({"error": "You can only edit your own posts."}, status=403)

        post.content = data["content"]
        post.save()

        return JsonResponse({"message": "Post edited successfully."}, status=200)


@csrf_exempt
def like(request, post_id):
    if request.method == "PUT":
        if not request.user.is_authenticated:
            return redirect(reverse("login"))

        post = Post.objects.get(id=post_id)

        liked = post.likes.filter(id=request.user.id).exists()

        if liked:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        message = "Post unliked successfully." if liked else "Post liked successfully."

        return JsonResponse( { 'liked' : not liked, 'likes' : post.get_likes() }, status=200)


def profile(request, username):
    if request.method == "GET":
        user = User.objects.get(username=username)
        posts = Post.objects.filter(author=user).order_by("-timestamp")

        response = {
            "user": user.serialize(),
            "posts": [],
        }

        for post in posts:
            current_post = post.serialize()
            current_post["liked"] = post.likes.filter(id=request.user.id).exists()
            response["posts"].append(current_post)

        if request.user.is_authenticated:
            response["user"]["followed"] = user.followers.filter(id=request.user.id).exists()
        else:
            response["user"]["followed"] = False

        return JsonResponse(response, safe=False)


@csrf_exempt
def follow(request):
    if request.method == "PUT":
        if not request.user.is_authenticated:
            return redirect(reverse("login"))

        data = json.loads(request.body)
        print(data)
        user = User.objects.get(username=data["username"])

        followed = request.user.following.filter(id=user.id).exists()

        if followed:
            request.user.following.remove(user)
        else:
            request.user.following.add(user)

        message = "User unfollowed successfully." if followed else "User followed successfully."

        return JsonResponse( { "message": message, 'followed' : not followed, 'followers' : user.get_followers() }, status=201)


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


def following(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            following = Post.objects.filter(author__in=request.user.following.all()).order_by("-timestamp")

            paginator = Paginator(following, 5)
            page_number = request.GET.get('page')
            number_of_pages = paginator.num_pages
            page_obj = paginator.get_page(page_number)

            response = {
                'num_pages': number_of_pages,
                'posts' : []
            }

            for post in page_obj:
                current_post = post.serialize()
                current_post["liked"] = post.likes.filter(id=request.user.id).exists()
                response["posts"].append(current_post)

            return JsonResponse(response, safe=False, status=200)
    return redirect(reverse("login"))