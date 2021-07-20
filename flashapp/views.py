from django.shortcuts import render, redirect, HttpResponse
from .models import FlashCard
import random
import csv
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    #cards = sorted(all_cards.order_by('front'), key=lambda x: random.random())
  
    return render(request, 'home.html')