from django.urls import path
from rest_framework.routers import SimpleRouter
from lms.views import (
    CourseViewSet,
    LessonListAPIView,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonUpdateAPIView,
    LessonRetrieveAPIView,
)
from lms.apps import LmsConfig

app_name = LmsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path(
        "lesson/retrieve/<int:pk>/",
        LessonRetrieveAPIView.as_view(),
        name="lesson_retrieve",
    ),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
]
urlpatterns += router.urls
