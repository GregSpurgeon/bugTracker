from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class MyUser(AbstractUser):
    pass


class Ticket(models.Model):
    ticket_choice = [
          ("New", 'New'),
          ('In Progress', 'In Progress'),
          ('Done', 'Done'),
          ('Invalid', 'Invalid')
    ]
    title = models.CharField(max_length=50)
    date_time_filed = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=50)
    user_who_filed = models.ForeignKey(MyUser, related_name="user_who_filed", on_delete=models.CASCADE)
    ticket_status_choice = models.CharField(max_length=100, choices=ticket_choice, default="New")
    assigned_user_ticket = models.ForeignKey(MyUser, related_name='assigned_user_ticket', blank=True, null=True, on_delete=models.CASCADE)
    user_who_completed = models.ForeignKey(MyUser, related_name='user_who_completed', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.assigned_user_ticket}'
