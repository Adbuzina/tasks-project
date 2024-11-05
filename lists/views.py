from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from lists.forms import TaskForm, TaskListForm
from lists.models import Task, TaskList


def index(request):
    return render(request, "lists/index.html", {"form": TaskForm()})


def tasklist(request, tasklist_id):
    tasklist = get_object_or_404(TaskList, pk=tasklist_id)
    if request.method == "POST":
        redirect("lists:add_task", tasklist_id=tasklist_id)

    return render(
        request, "lists/tasklist.html", {"tasklist": tasklist, "form": TaskForm()}
    )


def add_task(request, tasklist_id):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            task = Task(
                description=request.POST["description"],
                tasklist_id=tasklist_id,
                creator=user,
            )
            task.save()
            return redirect("lists:tasklist", tasklist_id=tasklist_id)
        else:
            return render(request, "lists/tasklist.html", {"form": form})

    return redirect("lists:index")


@login_required
def overview(request):
    if request.method == "POST":
        return redirect("lists:add_tasklist")
    return render(request, "lists/overview.html", {"form": TaskListForm()})


def new_tasklist(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            # create default tasklist
            user = request.user if request.user.is_authenticated else None
            tasklist = TaskList(creator=user)
            tasklist.save()
            task = Task(
                description=request.POST["description"],
                tasklist_id=tasklist.id,
                creator=user,
            )
            task.save()
            return redirect("lists:tasklist", tasklist_id=tasklist.id)
        else:
            return render(request, "lists/index.html", {"form": form})

    return redirect("lists:index")


def add_tasklist(request):
    if request.method == "POST":
        form = TaskListForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            tasklist = TaskList(title=request.POST["title"], creator=user)
            tasklist.save()
            return redirect("lists:tasklist", tasklist_id=tasklist.id)
        else:
            return render(request, "lists/overview.html", {"form": form})

    return redirect("lists:index")
