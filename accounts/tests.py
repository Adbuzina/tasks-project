from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.forms import LoginForm, RegistrationForm