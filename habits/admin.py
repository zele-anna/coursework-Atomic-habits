from django.contrib import admin

from habits.models import Action, Habit


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "is_enjoyable")


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "action", "associated_habit", "reward", "is_public")
