from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from web.models import User

# Create your views here.
def index(request):
    return render(request, "web/index.html")

def lesson(request):
    return render(request, "web/lesson.html")



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "web/login.html",
                {"message": "Invalid email and/or password."},
            )
    else:
        return render(request, "web/login.html")


@login_required(login_url="web/login.html")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        import re

        EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        username = request.POST["username"]

        # Ensure username, display name and location are long enough
        if len(username) < 3:
            return render(
                request,
                "web/register.html",
                {"message": "Username must be at least 3 characters long."},
            )

        email = request.POST["email"]

        # Ensure valid email address
        if email and not re.match(EMAIL_REGEX, email):
            return render(
                request, "web/register.html", {"message": "Not a valid email address."}
            )

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "web/register.html", {"message": "Passwords must match."}
            )

        if len(password) < 8:
            return render(
                request,
                "web/register.html",
                {"message": "Password must contain at least 8 characters."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username,
                email,
                password,
            )
            user.save()
        except IntegrityError:
            return render(
                request, "web/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "web/register.html")
