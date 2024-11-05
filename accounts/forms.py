from django import forms
from django.contrib.auth.models import User


def widget_attrs(placeholder):
    return {"class": "u-full-width", "placeholder": placeholder}


def form_kwargs(widget, label="", max_length=64):
    return {"widget": widget, "label": label, "max_length": max_length}


class LoginForm(forms.Form):

    username = forms.CharField(
        **form_kwargs(widget=forms.TextInput(attrs=widget_attrs("Логин")))
    )
    password = forms.CharField(
        **form_kwargs(widget=forms.PasswordInput(attrs=widget_attrs("Пароль")))
    )

    def clean(self):
        # Don't check if we already have errors.
        if self.errors:
            return self.cleaned_data

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
            raise forms.ValidationError("Неверное имя пользователя или пароль.")

        return self.cleaned_data


class RegistrationForm(forms.Form):

    username = forms.CharField(
        **form_kwargs(widget=forms.TextInput(attrs=widget_attrs("Логин")))
    )

    email = forms.EmailField(
        **form_kwargs(widget=forms.TextInput(attrs=widget_attrs("Email")))
    )

    password = forms.CharField(
        **form_kwargs(widget=forms.PasswordInput(attrs=widget_attrs("Пароль")))
    )

    password_confirmation = forms.CharField(
        **form_kwargs(
            widget=forms.PasswordInput(attrs=widget_attrs("Подтверждение пароля"))
        )
    )

    def clean(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")

        if password and password != password_confirmation:
            raise forms.ValidationError("Пароли не совпадают.")

        return self.cleaned_data
