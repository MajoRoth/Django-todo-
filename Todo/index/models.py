from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class Todo(models.Model):

    class PriorityLevels(models.IntegerChoices):
        Low = 1
        Moderate = 2
        Critical = 3

    class TimeUnits(models.IntegerChoices):
        M = 0
        H = 1

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    added_date = models.DateTimeField()
    text = models.CharField(max_length=200)
    priority = models.IntegerField(choices=PriorityLevels.choices, default=PriorityLevels.Low)
    est_time = models.IntegerField(default=0)
    est_time_unit = models.IntegerField(choices=TimeUnits.choices, default=TimeUnits.H)


class CreateUserFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


