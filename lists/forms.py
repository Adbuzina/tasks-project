from django import forms


def widget_attrs(placeholder):
    return {"class": "u-full-width", "placeholder": placeholder}


def form_kwargs(widget, label="", max_length=128):
    return {"widget": widget, "label": label, "max_length": max_length}


class TaskForm(forms.Form):
    description = forms.CharField(
        **form_kwargs(widget=forms.TextInput(attrs=widget_attrs("Введите задачу")))
    )


class TaskListForm(forms.Form):
    title = forms.CharField(
        **form_kwargs(
            widget=forms.TextInput(
                attrs=widget_attrs("Введите название для списка задач")
            )
        )
    )
