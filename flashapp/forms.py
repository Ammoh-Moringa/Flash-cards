from  django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic','bio','contact']
from django import forms
from .models import flashCard

class CreateNewDeck(forms.Form):
    name = forms.CharField(label="Name",max_length=200)

class CreateflashCard(forms.Form):
    question = forms.CharField(label = "Question", max_length=200)
    answer = forms.CharField(
            label = "Answer",
            widget = forms.Textarea )
