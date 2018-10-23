from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField(max_length=500)
    date_sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
