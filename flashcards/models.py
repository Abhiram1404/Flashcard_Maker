from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# FlashCard Model
class FlashCard(models.Model):
	category = models.CharField(max_length=50)
	front = models.TextField()
	back = models.TextField()
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.IntegerField(default=0)
	known = models.IntegerField(default=0)

	def __str__(self):
		return self.front

class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
