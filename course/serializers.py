from rest_framework import serializers
from typing import Any
from course import models
from users.models import User
from course.models import Course


class CourseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", 'first_name', 'last_name')


class CourseSerializer(serializers.ModelSerializer):
    is_buy = serializers.BooleanField()
    buy_user = CourseUserSerializer(many=True)
    buyers_count = serializers.IntegerField()

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'thumbnail',
            'content',
            'price',
            'price_discount',
            'is_buy',
            'buy_user',
            'buyers_count'
        )

    def to_representation(self, instance: Any) -> Any:
        json = super().to_representation(instance)
        json['buy_user'] = json['buy_user'][:5]
        return json
