from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Action(models.Model):
    title = models.CharField(max_length=255, verbose_name="Действие")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", blank=True, null=True)
    is_enjoyable = models.BooleanField(verbose_name="Признак приятной привычки", default=False)

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"

    def __str__(self):
        return self.title


class Habit(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", blank=True, null=True)
    action = models.ForeignKey(Action, on_delete=models.CASCADE, verbose_name="Действие")
    time_to_start = models.TimeField(verbose_name="Время начала", blank=True, null=True)
    place = models.CharField(max_length=255, verbose_name="Место выполнения", blank=True, null=True)
    associated_habit = models.ForeignKey(
        Action,
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        blank=True,
        null=True,
        related_name="associated_habit",
    )
    periodicity = models.PositiveSmallIntegerField(
        verbose_name="Периодичность", default=1, validators=[MinValueValidator(1), MaxValueValidator(7)]
    )
    reward = models.CharField(max_length=255, verbose_name="Вознаграждение", blank=True, null=True)
    time_to_complete = models.PositiveSmallIntegerField(
        verbose_name="Время на выполнение", default=60, validators=[MinValueValidator(1), MaxValueValidator(120)]
    )
    is_public = models.BooleanField(verbose_name="Признак публичности", default=False)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return self.action.title
