from django.db import models
from django.contrib.auth.models import User

class deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deck", null=True)
    name = models.CharField(max_length=200)
    

    def __str__(self):
        return self.name

class flashCard(models.Model):
    deck = models.ForeignKey(deck, on_delete=models.CASCADE, related_name="flashCard", null=True)
    question = models.CharField(max_length = 200)
    answer = models.TextField()
    

    def __str__(self):
        return self.question