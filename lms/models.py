from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    image = models.ImageField(upload_to="lms/image", verbose_name="Превью", **NULLABLE)
    description = models.TextField(verbose_name="Oписание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="lms/image", verbose_name="Превью", **NULLABLE)
    url = models.URLField(verbose_name="Ссылка на видео", **NULLABLE)
    course = models.ForeignKey(Course, verbose_name="Курс", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
