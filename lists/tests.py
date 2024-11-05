from unittest import skip

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from lists.forms import TaskForm, TaskListForm
from lists.models import Task, TaskList


class ListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", "test@example.com", "test")
        self.tasklist = TaskList(title="test title", creator=self.user)
        self.tasklist.save()
        self.task = Task(description="save task", tasklist_id=self.tasklist.id, creator=self.user)
        self.task.save()
        self.client.login(username="test", password="test")

    def tearDown(self):
        self.client.logout()
        self.user.delete()
        self.tasklist.delete()
        self.task.delete()

    def test_get_index_page(self):
        response = self.client.get(reverse("lists:index"))
        self.assertTemplateUsed(response, "lists/index.html")
        self.assertIsInstance(response.context["form"], TaskForm)

    def test_add_task_to_index_page(self):
        response = self.client.post(reverse("lists:index"), {"description": "test"})
        self.assertTemplateUsed(response, "lists/index.html")
        self.assertIsInstance(response.context["form"], TaskForm)

    def test_get_tasklist_view(self):
        response = self.client.get(reverse("lists:tasklist", kwargs={"tasklist_id": self.tasklist.id}))
        self.assertTemplateUsed(response, "lists/tasklist.html")
        self.assertIsInstance(response.context["form"], TaskForm)

    def test_add_task_to_tasklist_view(self):
        response = self.client.post(
            reverse("lists:tasklist", kwargs={"tasklist_id": self.tasklist.id}),
            {"description": "test"},
        )
        self.assertTemplateUsed(response, "lists/tasklist.html")
        self.assertIsInstance(response.context["form"], TaskForm)
        self.assertContains(response, "test")

    def test_get_tasklist_overview(self):
        response = self.client.get(reverse("lists:overview"))
        self.assertTemplateUsed(response, "lists/overview.html")
        self.assertIsInstance(response.context["form"], TaskListForm)

    def test_get_tasklist_overview_redirect_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("lists:overview"))
        self.assertRedirects(response, "/auth/login/?next=/tasklists/")

    def test_add_tasklist_to_tasklist_overview(self):
        response = self.client.post(reverse("lists:overview"), {"title": "some title"})
        self.assertRedirects(
            response,
            "/tasklist/add/",
            target_status_code=302,
            fetch_redirect_response=False,
        )


class TaskListFormTests(TestCase):
    def setUp(self):
        self.vaild_form_data = {"title": "some title"}
        self.too_long_title = {"title": 129 * "X"}

    def test_valid_input(self):
        form = TaskListForm(self.vaild_form_data)
        self.assertTrue(form.is_valid())

    def test_no_title(self):
        form = TaskListForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"title": ["This field is required."]})

    def test_empty_title(self):
        form = TaskListForm({"title": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"title": ["This field is required."]})


class TaskFormTests(TestCase):
    def setUp(self):
        self.valid_form_data = {"description": "something to be done"}
        self.too_long_description = {"description": 129 * "X"}

    def test_valid_input(self):
        form = TaskForm(self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_no_description(self):
        form = TaskForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"description": ["This field is required."]})

    def test_empty_description(self):
        form = TaskForm({"description": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"description": ["This field is required."]})

    def test_too_title(self):
        form = TaskForm(self.too_long_description)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "description": [
                    "Ensure this value has at most 128 " + "characters (it has 129)."
                ]
            },
        )


class ListModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", "test@example.com", "test")
        self.tasklist = TaskList(title="title", creator=self.user)
        self.tasklist.save()
        self.task = Task(
            description="description", tasklist_id=self.tasklist.id, creator=self.user
        )
        self.task.save()

    def tearDown(self):
        self.task.delete()
        self.tasklist.delete()
        self.user.delete()

    def test_count_tasks(self):
        self.assertEqual(self.tasklist.count(), 1)
        new_task = Task(
            description="test", tasklist_id=self.tasklist.id, creator=self.user
        )
        new_task.save()
        self.assertEqual(self.tasklist.count(), 2)

    def test_count_open_tasks(self):
        self.assertEqual(self.tasklist.count_open(), 1)
        new_task = Task(
            description="test", tasklist_id=self.tasklist.id, creator=self.user
        )
        new_task.save()
        self.assertEqual(self.tasklist.count_open(), 2)
        new_task.close()
        self.assertEqual(self.tasklist.count_open(), 1)

    def test_count_closed_tasks(self):
        self.assertEqual(self.tasklist.count_finished(), 0)
        new_task = Task(
            description="test", tasklist_id=self.tasklist.id, creator=self.user
        )
        new_task.close()
        self.task.close()
        self.assertEqual(self.tasklist.count_finished(), 2)
        self.assertIsNotNone(new_task.finished_at)
        self.task.reopen()
        self.assertEqual(self.tasklist.count_finished(), 1)
        self.assertIsNone(self.task.finished_at)
