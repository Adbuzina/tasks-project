from django.urls import path

from lists import views

app_name = "lists"
urlpatterns = [
    path("", views.index, name="index"),
    path("tasklist/<int:tasklist_id>/", views.tasklist, name="tasklist"),
    path("tasklist/new/", views.new_tasklist, name="new_tasklist"),
    path("tasklist/add/", views.add_tasklist, name="add_tasklist"),
    path("task/add/<int:tasklist_id>/", views.add_task, name="add_task"),
    path("tasklists/", views.overview, name="overview"),
]
