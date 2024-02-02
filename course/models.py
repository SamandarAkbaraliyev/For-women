from django.db import models
from main.models import BaseModel
from users.models import User
from main.models import Category
from django.db.models.signals import post_save
from django.dispatch import receiver
from moviepy.editor import VideoFileClip


class Course(BaseModel):
    class Language(models.TextChoices):
        UZ = 'Uzbek'
        RU = 'Russian'
        EN = 'English'

    category_of_course = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=55)
    content = models.TextField()

    thumbnail = models.FileField(upload_to='courses/', null=True, blank=True, default='thumbnail/download')
    price = models.PositiveIntegerField(null=True)
    price_discount = models.PositiveIntegerField(null=True, blank=True)

    language = models.CharField(max_length=10, choices=Language.choices, default=Language.UZ)
    buy_user = models.ManyToManyField(User, related_name='buy_course', blank=True)

    def __str__(self):
        return self.title


class Comment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    course_of_comment = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', null=True)

    def __str__(self):
        return f"{self.author}'s comment"

    def get_comments(self):
        return Comment.objects.filter(parent_comment=self).filter(active=True)


class Lesson(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)

    course_of_lesson = models.ForeignKey(Course, on_delete=models.CASCADE,
                                         related_name='lessons')
    video = models.FileField(upload_to='course/videos/', default='templates/users/Azimjohn.MP4', blank=True)
    description = models.TextField(null=True)

    totel_time = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title


class LessonUser(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_us = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_user')
    time_watched = models.IntegerField(default=0)
    paused_time = models.IntegerField(default=0)
    totel_time = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f"{self.user} - {self.lesson}"

    def is_finished(self):
        return self.totel_time * 0.9 <= self.time_watched

    @property
    def status(self):
        if self.is_finished():
            return "Finished"
        if self.time_watched > 0:
            return "In progress"
        return "Not started"


class LessonUserWatched(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_user = models.ForeignKey(LessonUser, on_delete=models.CASCADE)

    from_time = models.IntegerField(default=0)
    to_time = models.IntegerField(default=0)


@receiver(post_save, sender=Lesson)
def calculate_video_length(sender, instance, created, **kwargs):
    if created:
        video = VideoFileClip(instance.video.path)
        instance.totel_time = video.duration
        instance.save()
