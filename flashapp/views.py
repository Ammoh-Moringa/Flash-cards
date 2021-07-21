from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import deck, flashCard
from .forms import CreateNewDeck, CreateflashCard

def home(response):
    if response.method == "POST":
        form = CreateNewDeck(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = deck(name=n)
            t.save()
            response.user.deck.add(t)
        return HttpResponseRedirect("/")
    
    else:
        form = CreateNewDeck()
    return render(response, "home.html", {"form": form })