from django.urls import path
from course.views import (
    CourseListAPIView,
)

urlpatterns = [
    path("", CourseListAPIView.as_view()),
]
