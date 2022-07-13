from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Lesson(models.Model):
    title = models.CharField(blank=False, max_length=128)
    introduction = models.TextField(blank=False)
    main_text = models.TextField(blank=False)
    required_score = models.IntegerField(default=0, blank=False)
    completed = models.ManyToManyField(User, related_name="completed", blank=True)
    image = models.CharField(blank=True, max_length=128)
    # image/video
    # has_video

    def is_completed(self):
        return self.completed.filter(completed=True, creator=User)

    def __str__(self):
        return f"{self.title}"


# Tests
# Seperate model?
# Seperate page, quiz and check via view if score is big
