from django import forms
from .models import flashCard

class CreateNewDeck(forms.Form):
    name = forms.CharField(label="Name",max_length=200)

class CreateflashCard(forms.Form):
    question = forms.CharField(label = "Question", max_length=200)
    answer = forms.CharField(
            label = "Answer",
            widget = forms.Textarea )