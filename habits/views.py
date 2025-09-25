from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.pagination import CustomPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    '''Эндпоинт-сет для работы с привычками.'''
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [
                IsAuthenticated,
            ]
        elif self.action in [
            "retrieve",
            "update",
            "partial_update",
            "destroy",
        ]:
            self.permission_classes = [
                IsOwner,
            ]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class PublicHabitListAPIView(ListAPIView):
    '''Эндпоинт для отображения списка публичных привычек.'''
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = CustomPagination
    permission_classes = [
        AllowAny,
    ]
