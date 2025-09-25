from rest_framework import serializers


def validate_associated_or_reward(value):
    """Валидация заполнения только одного из полей - связанной привычки или вознаграждения."""
    associated_habit = dict(value).get("associated_habit")
    reward = dict(value).get("reward")
    if associated_habit and reward:
        raise serializers.ValidationError("Нельзя одновременно выбрать связанную привычку и указать вознаграждение")


def validate_associated_is_enjoyable(value):
    """Валидация признака приятности связанной привычки."""
    associated_habit = dict(value).get("associated_habit")
    if associated_habit and not associated_habit.is_enjoyable:
        raise serializers.ValidationError("Связанная привычка должна быть приятной")


def validate_enjoyable_habit_no_reward(value):
    """Валидация приятной привычки - не может быть вознаграждения или связанной привычки."""
    action = dict(value).get("action")
    is_enjoyable = action.is_enjoyable
    reward = dict(value).get("reward")
    associated_habit = dict(value).get("associated_habit")
    if is_enjoyable:
        if reward or associated_habit:
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )
