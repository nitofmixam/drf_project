from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson, Subscribe
from lms.validators import LinkValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkValidator(field='url')]


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lesson = LessonSerializer(source="lesson_set", read_only=True, many=True)
    subscribe = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, object):
        if object.lesson_set.count():
            return object.lesson_set.count()
        return 0

    def get_subscribe(self, instance):
        request = self.context.get('request')
        user = None

        if request:
            user = request.user
        return instance.subscribe_set.filter(user=user).exists()


class SubscribeSerializer(ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'
