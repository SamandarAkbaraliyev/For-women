from rest_framework import serializers
from typing import Any
from users.models import User
from course.models import Course, Lesson, LessonUser, Comment
from django.utils import timezone


class CourseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", 'first_name', 'last_name')


class CourseSerializer(serializers.ModelSerializer):
    is_buy = serializers.BooleanField()
    buy_user = CourseUserSerializer(many=True)
    buyers_count = serializers.IntegerField()
    author = CourseUserSerializer()

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'thumbnail',
            'content',
            'price',
            'price_discount',
            'category_of_course',
            'is_buy',
            'buy_user',
            'buyers_count'
        )

    def to_representation(self, instance: Any) -> Any:
        json = super().to_representation(instance)
        json['buy_user'] = json['buy_user'][:5]
        return json


class LessonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonUser
        fields = ('time_watched', 'totel_time', 'status')


class LessonCourseSerializer(serializers.ModelSerializer):
    lesson_user = LessonUserSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ('title', 'video', 'description', 'totel_time', 'lesson_user')


class CourseCommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    time_since_created = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'time_since_created')

    def get_time_since_created(self, obj):
        current_time = timezone.now()
        time_difference = (current_time - obj.created_at).total_seconds()

        if time_difference < 60:
            return f"{int(time_difference)} seconds ago"
        elif time_difference < 3600:
            return f"{int(time_difference // 60)} minutes ago"
        elif time_difference < 86400:
            return f"{int(time_difference // 3600)} hours ago"
        elif time_difference > 86400:
            return f"{int(time_difference // 86400)} days ago"
        else:
            return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'title',
            'category_of_course',
            'thumbnail',
            'content',
            'price',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        course = Course.objects.create(author_id=user.id, **validated_data)
        return course


class CourseRetrieveSerializer(serializers.ModelSerializer):
    author = CourseUserSerializer()
    is_buy = serializers.BooleanField()
    lessons = LessonCourseSerializer(many=True)
    category_of_course = serializers.CharField(source='category_of_course.name')
    comments = CourseCommentSerializer(many=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'category_of_course',
            'title',
            'content',
            'thumbnail',
            'price',
            'language',
            'is_buy',
            'lessons',
            'comment_count',
            'comments',
        )

    def get_comment_count(self, obj):
        return obj.comments.count()


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']

    def create(self, validated_data):
        request = self.context.get('request')
        course_id = self.context.get('course_id')

        author = request.user
        course = Course.objects.get(id=course_id)

        instance = Comment.objects.create(author=author, course_of_comment=course, **validated_data)

        parent_comment_id = request.GET.get('parent_comment_id')
        if parent_comment_id:
            instance.parent_comment.id = parent_comment_id
        instance.save()
        return instance


class LessonWatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonUser
        fields = ('user', 'paused_time', 'totel_time', 'status', 'time_watched', 'lesson_us')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        lesson_id = self.context.get('lesson_id')
        lesson = Lesson.objects.get(id=lesson_id)
        print(lesson_id)

        instance = LessonUser.objects.create(user=user, lesson_us=lesson)

        return instance
