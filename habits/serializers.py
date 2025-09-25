from rest_framework import serializers

# from habits.models import Action, Habit
from habits.models import Habit
from habits.validators import (validate_associated_is_enjoyable, validate_associated_or_reward,
                               validate_enjoyable_habit_no_reward)


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            validate_associated_or_reward,
            validate_associated_is_enjoyable,
            validate_enjoyable_habit_no_reward,
        ]
