from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from course.utils import MultipartJsonParser, parsers
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView
from course.models import Course, Comment, Lesson, LessonUser
from course.serializers import (
    CourseSerializer,
    CourseCreateSerializer,
    CourseRetrieveSerializer,
    CommentCreateSerializer,
    LessonWatchSerializer
)
from django.db import models
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ("category", "status")

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                is_buy=models.Case(
                    models.When(buy_user=self.request.user, then=True),
                    default=False,
                    output_field=models.BooleanField(),
                ),
                buyers_count=models.Count("buy_user"),
            )
        )


class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAdminUser]


class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseRetrieveSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                is_buy=models.Case(
                    models.When(buy_user=self.request.user, then=True),
                    default=False,
                    output_field=models.BooleanField(),
                )
            )
        )


class CommentPostAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = None

    def get_serializer_context(self):
        return {'request': self.request,
                'course_id': self.kwargs.get('course_id')}


class LessonWatchCreateAPIView(CreateAPIView):
    queryset = LessonUser.objects.all()
    serializer_class = LessonWatchSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = None

    def get_serializer_context(self):
        return {'request': self.request,
                'lesson_id': self.kwargs.get('lesson_id')}


class LessonWatchUpdateAPIView(RetrieveUpdateAPIView):
    queryset = LessonUser.objects.all()
    serializer_class = LessonWatchSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = None

    def get_serializer_context(self):
        return {'request': self.request,
                'lesson_id': self.kwargs.get('lesson_id')}
