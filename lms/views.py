from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from lms.models import Course, Lesson, Subscribe
from lms.paginators import LmsPaginator
from lms.permissions import IsModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer, SubscribeSerializer


class CourseViewSet(ModelViewSet):
    """
    View set for a Course
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LmsPaginator

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "list", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        if self.action == "destroy":
            self.permission_classes = [~IsModerator | IsOwner]
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """
    Lesson create endpoint
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonUpdateAPIView(UpdateAPIView):
    """
    Lesson update endpoint
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonListAPIView(ListAPIView):
    """
    Lesson list endpoint
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = LmsPaginator

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    Lesson retrieve endpoint
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    """
    Lesson delete endpoint
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator | IsOwner]


class SubscribeCreateAPIView(CreateAPIView):
    """
    Subscribe create endpoint
    """

    serializer_class = SubscribeSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        subscribe, created = Subscribe.objects.get_or_create(
            user=user, course=course_item
        )
        if not created:
            subscribe.delete()
            message = "Subscribe deleted successfully"

        else:
            message = "Subscribe created successfully"

        return Response({"message": message})