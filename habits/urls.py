from django.urls import path
from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import ActionViewSet, HabitViewSet, PublicHabitListAPIView

app_name = HabitsConfig.name

router_actions = SimpleRouter()
router_actions.register("actions", ActionViewSet)
router_habits = SimpleRouter()
router_habits.register("", HabitViewSet)

urlpatterns = [
    path("public/", PublicHabitListAPIView.as_view(), name="public-habits"),
]

urlpatterns += router_actions.urls
urlpatterns += router_habits.urls
