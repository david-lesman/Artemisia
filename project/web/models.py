from django.contrib.auth.models import AbstractUser
from django.db import models
from regex import F

# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

    def get_required_lessons_test(self, test):
        for x in test.required_lessons.all():
            if self not in x.completed:
                return False

        return True


class Lesson(models.Model):
    title = models.CharField(blank=False, max_length=128)
    introduction = models.TextField(blank=False)
    main_text = models.TextField(blank=False)
    required_lessons = models.ManyToManyField(
        "self", related_name="required", blank=True
    )
    completed = models.ManyToManyField(User, related_name="completed", blank=True)
    image = models.CharField(blank=True, max_length=128)
    video = models.CharField(blank=True, max_length=128)
    icon = models.CharField(blank=True, max_length=32)
    has_video = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return f"{self.title}"


class Answer(models.Model):
    content = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"answer: {self.content}, correct: {self.correct}"


class Question(models.Model):
    content = models.CharField(max_length=200)
    answers = models.ManyToManyField(Answer, related_name="question")

    def __str__(self):
        return self.content

    def get_answers(self):
        return self.answers.all()


class Test(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    questions = models.ManyToManyField(Question, related_name="test")
    completed = models.ManyToManyField(User, related_name="completed_tests", blank=True)
    required_lessons = models.ManyToManyField(
        Lesson, related_name="required", blank=True
    )

    def __str__(self):
        return f"{self.name}"

    def get_questions(self):
        return self.questions.all()
