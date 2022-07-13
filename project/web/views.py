from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from web.models import User, Lesson

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        lessons = request.user.completed.all()
        lessons = [i.id for i in lessons]
        lessons = [1, 2, 3, 4]
        return render(request, "web/dashboard.html", {"lessons": lessons})

    return render(request, "web/index.html")


@login_required(login_url="login")
def lesson(request, lesson_id):
    if request.method == "POST":
        # Check if score on quiz is good
        lesson = Lesson.objects.get(pk=lesson_id)
        score = int(request.POST["score"])
        if score >= lesson.required_score:
            lesson.completed.add(request.user)
            return HttpResponseRedirect(reverse("index"))

    lesson = Lesson.objects.get(pk=lesson_id)
    chopped_text = [i.strip() for i in lesson.main_text.split("@")]  # @ is seperator
    return render(
        request, "web/lesson.html", {"lesson": lesson, "small_text": chopped_text}
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if request.POST.get("next"):
                return HttpResponseRedirect(request.POST["next"])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "web/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "web/login.html")


@login_required(login_url="login")
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
