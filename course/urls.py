from django.urls import path
from course.views import (
    CourseListAPIView,
    CourseCreateAPIView,
    CourseRetrieveAPIView,
    CommentPostAPIView,
    LessonWatchCreateAPIView
)

urlpatterns = [
    path("", CourseListAPIView.as_view()),
    path("create/", CourseCreateAPIView.as_view()),
    path('detail/<int:pk>/', CourseRetrieveAPIView.as_view()),

    path('detail/<int:course_id>/post/comment/', CommentPostAPIView.as_view()),

    path('lesson/<int:lesson_id>/watch/', LessonWatchCreateAPIView.as_view())
]
