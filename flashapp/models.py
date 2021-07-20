from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# FlashCard Model
class FlashCard(models.Model):
	category = models.CharField(max_length=50)
	front = models.TextField()
	back = models.TextField()
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=timezone.now())

	def __str__(self):
		return self.front