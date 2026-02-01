from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    ]

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Employee')

    def __str__(self):
        role_display = self.role if self.role else "No Role"
        return f"{self.username} ({role_display})"

    @property
    def is_manager(self):
        return self.role == 'Manager'

    @property
    def is_employee(self):
        return self.role == 'Employee'


class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['due_date'] #חוסך מיון לפי תאריך