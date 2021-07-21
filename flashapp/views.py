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


def createFlash(response, id):
    form = CreateflashCard()
    s_deck = get_object_or_404(deck, id=id)
    if not response.user.is_authenticated:
        return HttpResponseRedirect("/")
    if s_deck not in response.user.deck.all():
        return HttpResponseRedirect("/")
    if response.method == "POST":
        form = CreateflashCard(response.POST)
        if form.is_valid():
            card = flashCard(
                    deck = s_deck,
                    question = form.cleaned_data["question"],
                    answer = form.cleaned_data["answer"]
                )
            card.save() 
        form = CreateflashCard()
    context = {"id":id,"deck":s_deck, "form":form}
    return render(response, "flashcreate.html", context)


def updateFlash(response, id):
    card = get_object_or_404(flashCard, id=id)
    initial_data = {
            "question" : card.question,
            "answer" : card.answer
             }
    form = CreateflashCard(response.POST or None, initial=initial_data)
    context = {"form":form}
    if not response.user.is_authenticated:
        return HttpResponseRedirect("/")
    elif card.deck not in response.user.deck.all():
        return HttpResponseRedirect("/")
    else:
        if response.method == "POST":
            form = CreateflashCard(response.POST)
            if form.is_valid():
                card.question = form.cleaned_data["question"]
                card.answer = form.cleaned_data["answer"]
                card.save()
            #if response.POST.get("name") 
           
            return HttpResponseRedirect("/deck-%d" %card.deck.id)
    return render(response, "flashupdate.html", context)