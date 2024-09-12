from celery import shared_task
from django.core.mail import send_mail

from config import settings
from lms.models import Subscribe


@shared_task
def send_mail_about_course(course):
    subscriptions = Subscribe.objects.filter(course=course)
    if subscriptions:
        course_name = subscriptions[0].course.title
        emails = []
        for subscription in subscriptions:
            emails.append(subscription.user.email)
        send_mail(
            f"Обновление курса {course_name}",
            f"Добавлен новый урок в курс {course_name}",
            settings.EMAIL_HOST_USER,
            emails,
        )
