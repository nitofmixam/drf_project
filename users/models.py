from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    country = models.CharField(
        max_length=30,
        verbose_name="Страна",
        blank=True,
        null=True,
        help_text="Укажите страну проживания",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите аватарку",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course, verbose_name="Курс", on_delete=models.CASCADE, blank=True, null=True
    )
    lesson = models.ForeignKey(
        Lesson,
        verbose_name="Урок",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    total_price = models.FloatField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=50, verbose_name="Способ оплаты")

    def __str__(self):
        return (
            f"{self.user} - {self.course if self.course else self.lesson} = "
            f"{self.total_price}$"
        )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
