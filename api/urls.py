from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"tasklists", views.TaskListViewSet)
router.register(r"tasks", views.TaskViewSet)

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
]
