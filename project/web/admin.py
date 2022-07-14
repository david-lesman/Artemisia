from django.contrib import admin
from .models import User, Lesson, Test, Question, Answer

# Register your models here.
admin.site.register(User)
admin.site.register(Lesson)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
