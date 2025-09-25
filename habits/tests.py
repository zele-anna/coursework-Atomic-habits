from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test1@example.com")
        self.habit = Habit.objects.create(action="Habit 1", owner=self.user)
        self.habit_enj = Habit.objects.create(action="Habit enjoyable", is_enjoyable=True, owner=self.user)

        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        """Тестирование создания привычки."""
        data = {"action": "Habit test"}
        response = self.client.post("/habits/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 3)

    def test_habit_retrieve(self):
        """Тестирование получения информации по привычке."""
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Habit 1")
        self.assertEqual(data.get("place"), None)
        self.assertEqual(data.get("is_enjoyable"), False)

    def test_habit_update(self):
        """Тестирование изменения привычки."""
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        data = {"associated_habit": self.habit_enj.pk}
        response = self.client.patch(url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 2)
        self.assertEqual(result.get("associated_habit"), self.habit_enj.pk)

    def test_habit_delete(self):
        """Тестирование удаления привычки."""
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_habit_list(self):
        """Тестирование вывода списка привычек."""
        response = self.client.get("/habits/")
        result = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "action": "Habit 1",
                    "time_to_start": None,
                    "place": None,
                    "is_enjoyable": False,
                    "periodicity": 1,
                    "reward": None,
                    "time_to_complete": 60,
                    "is_public": False,
                    "owner": self.user.pk,
                    "associated_habit": None,
                },
                {
                    "id": self.habit_enj.pk,
                    "action": "Habit enjoyable",
                    "time_to_start": None,
                    "place": None,
                    "is_enjoyable": True,
                    "periodicity": 1,
                    "reward": None,
                    "time_to_complete": 60,
                    "is_public": False,
                    "owner": self.user.pk,
                    "associated_habit": None,
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), result)


class HabitPublicTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test1@example.com")
        self.habit = Habit.objects.create(action="Habit 1", owner=self.user)
        self.habit_pub = Habit.objects.create(action="Habit public", is_public=True, owner=self.user)

        # self.client.force_authenticate(user=self.user)

    def test_habit_list(self):
        """Тестирование вывода списка публичных привычек."""
        response = self.client.get("/habits/public/")
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit_pub.pk,
                    "action": "Habit public",
                    "time_to_start": None,
                    "place": None,
                    "is_enjoyable": False,
                    "periodicity": 1,
                    "reward": None,
                    "time_to_complete": 60,
                    "is_public": True,
                    "owner": self.user.pk,
                    "associated_habit": None,
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), result)
