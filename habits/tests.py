from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Action, Habit
from users.models import User


class ActionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test1@example.com")
        self.action = Action.objects.create(title='Action 1', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_action_create(self):
        '''Тестирование создания действия.'''
        data = {'title': 'Test action 1'}
        response = self.client.post('/habits/actions/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Action.objects.all().count(), 2)

    def test_action_retrieve(self):
        '''Тестирование получения информации по действию.'''
        url = reverse('habits:action-detail', args=(self.action.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), self.action.title)
        self.assertEqual(data.get('is_enjoyable'), False)

    def test_action_update(self):
        '''Тестирование изменения действия.'''
        url = reverse('habits:action-detail', args=(self.action.pk,))
        data = {'title': 'Test action update'}
        response = self.client.patch(url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Action.objects.all().count(), 1)
        self.assertEqual(result.get('title'), 'Test action update')

    def test_action_delete(self):
        '''Тестирование удаления действия.'''
        url = reverse('habits:action-detail', args=(self.action.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Action.objects.all().count(), 0)

    def test_action_list(self):
        '''Тестирование вывода списка действий.'''
        response = self.client.get('/habits/actions/')
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results':
                [
                    {
                        'id': self.action.pk,
                        'title': 'Action 1',
                        'is_enjoyable': False,
                        'owner': self.user.pk
                    }
                ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), result)


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test1@example.com")
        self.action = Action.objects.create(title='Action 1', owner=self.user)
        self.action_enj = Action.objects.create(title='Action enjoyable', owner=self.user, is_enjoyable=True)
        self.habit = Habit.objects.create(action=self.action, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        '''Тестирование создания привычки.'''
        data = {'action': self.action.pk}
        response = self.client.post('/habits/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Action.objects.all().count(), 2)

    def test_habit_retrieve(self):
        '''Тестирование получения информации по привычке.'''
        url = reverse('habits:habit-detail', args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('action'), self.action.pk)
        self.assertEqual(data.get('place'), None)

    # def test_habit_update(self):
    #     '''Тестирование изменения привычки.'''
    #     url = reverse('habits:habit-detail', args=(self.habit.pk,))
    #     data = {'associated_habit': self.action_enj.pk}
    #     response = self.client.patch(url, data=data)
    #     result = response.json()
    #     print(result)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # self.assertEqual(Habit.objects.all().count(), 1)
        # self.assertEqual(result.get('associated_habit'), self.action_enj.pk)

    # def test_action_delete(self):
    #     '''Тестирование удаления действия.'''
    #     url = reverse('habits:action-detail', args=(self.action.pk,))
    #     response = self.client.delete(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Action.objects.all().count(), 0)
    #
    # def test_action_list(self):
    #     '''Тестирование вывода списка действий.'''
    #     response = self.client.get('/habits/actions/')
    #     result = {
    #         'count': 1,
    #         'next': None,
    #         'previous': None,
    #         'results':
    #             [
    #                 {
    #                     'id': self.action.pk,
    #                     'title': 'Action 1',
    #                     'is_enjoyable': False,
    #                     'owner': self.user.pk
    #                 }
    #             ]
    #     }
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.json(), result)
