from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from web.models import Test, User, Lesson


def check_required_complete(request, object) -> bool:
    lessons = request.user.completed.all()
    tests = request.user.completed_tests.all()
    lessons = [i.id for i in lessons]  # user completed lessons/tests
    for test in tests:
        lessons.append(4 * test.id)

    for x in object.required_lessons.all():
        if x.id not in lessons:
            return False

    return True


# Create your views here.
def index(request, message: str = None):
    if request.user.is_authenticated:
        clessons = request.user.completed.all()
        tests = request.user.completed_tests.all()
        lessons = [i.id for i in clessons]
        for test in tests:
            lessons.append(4 * test.id)
        return render(
            request,
            "web/dashboard.html",
            {
                "lessons": lessons,
                "message": message,
            },
        )

    return render(request, "web/index.html")


def about(request):
    return render(request, "web/about.html")


@login_required(login_url="login")
def lesson(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    if request.method == "POST":
        lesson.completed.add(request.user)
        return HttpResponseRedirect(reverse("index"))

    if not check_required_complete(request, lesson):
        message = "You haven't completed the required lessons yet."
        return index(request, message)

    chopped_text = [i.strip() for i in lesson.main_text.split("@")]  # @ is seperator
    return render(
        request, "web/lesson.html", {"lesson": lesson, "small_text": chopped_text}
    )


@login_required(login_url="login")
def test(request, test_id):
    test = Test.objects.get(pk=test_id)
    if request.method == "POST":
        score = 0
        wrong_questions = []
        for i in range(len(test.get_questions())):
            answer = request.POST.get(f"{i + 1}")  # Loop starts at 0, ids start at 1
            q = test.questions.get(pk=(i + 1))
            correct_answer = q.answers.get(correct=True)

            if answer == correct_answer.content:
                score += 1
            else:  # Didn't answer question or got question wrong
                wrong_questions.append(q)

        # Check if score is high enough
        if score / len(test.get_questions()) >= 0.75:
            test.completed.add(request.user)
            message = (
                f"You scored {score / len(test.get_questions()) * 100}%. \n Well done!"
            )
        else:
            message = f"You scored {score / len(test.get_questions()) * 100}%. Review your lessons and try again!"

        return render(request, "web/results.html", {"message": message})

    if not check_required_complete(request, test):
        message = "You haven't completed the required lessons yet."
        return index(request, message)

    return render(request, "web/test.html", {"test": test})


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
