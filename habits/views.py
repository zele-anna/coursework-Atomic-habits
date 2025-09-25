from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Action, Habit
from habits.pagination import CustomPagination
from habits.serializers import ActionSerializer, HabitSerializer
from users.permissions import IsOwner


class ActionViewSet(ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
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
        action = serializer.save()
        action.owner = self.request.user
        action.save()

    def get_queryset(self):
        return Action.objects.filter(owner=self.request.user)


class HabitViewSet(ModelViewSet):
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
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = CustomPagination
    permission_classes = [
        AllowAny,
    ]
