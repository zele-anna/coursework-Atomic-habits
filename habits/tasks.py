import json

import requests
from celery import shared_task
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from config.settings import TELEGRAM_TOKEN, TELEGRAM_URL
from habits.models import Habit


@shared_task
def create_periodic_task():
    """Создание периодических задач по привычкам."""
    habits = Habit.objects.all()

    for habit in habits:
        # Перебираем привычки и проверяем, указан ли у пользователя chat_id
        # и не создана ли по привычке периодическая задача
        if (
            habit.owner.chat_id
            and not PeriodicTask.objects.filter(
                name=f"Напоминание о задаче {habit.pk} для {habit.owner.chat_id}"
            ).exists()
        ):
            print(f"Создание напоминания о задаче {habit.pk} для {habit.owner.chat_id}")
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=habit.periodicity,
                period=IntervalSchedule.DAYS,
            )

            message = f"Я буду {habit.action} в {habit.time_to_start} в {habit.place}!"

            # Создаем задачу для повторения
            PeriodicTask.objects.create(
                interval=schedule,
                name=f"Напоминание о задаче {habit.pk} для {habit.owner.chat_id}",
                task="habits.tasks.send_tg_notification",
                args=json.dumps([habit.owner.chat_id, message]),
                start_time=str(timezone.now().date()) + " " + str(habit.time_to_start),
            )


@shared_task
def send_tg_notification(chat_id, message):
    """Задача по отправке уведомления в Телеграм о выполнении привычки."""
    params = {"chat_id": chat_id, "text": message}
    requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)
