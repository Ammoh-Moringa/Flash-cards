from django.http.response import Http404
from flashapp.serializer import ProfileSerializer
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import  HttpResponseRedirect
from .models import deck, flashCard
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from flashapp.forms import CreateNewDeck, CreateUserForm, CreateflashCard, ProfileForm
from .models import Profile
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import flashCardSerializer
from rest_framework import status
# Create your views here.
from .models import  deck
from .serializer import DeckSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginpage')
        name = form.cleaned_data.get("username")
        messages.success(request, 'Account was created for' , name)
    context = {'form':form, 'profile':profile}
    return render(request, 'accounts/register.html', context)
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Incorrect Username or Password')
    context = {}
    return render(request, 'accounts/login.html', context)
def logoutpage(request):
    logout(request)
    return redirect('loginpage')
def profile(request):
    try:
        profile = request.user.profile
    except ProfileForm.DoesNotExist:
        profile = Profile(user=request.user)
    user = request.user
    if request.method == 'POST':
        prof_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return redirect(request.path_info)
    else:
        prof_form = ProfileForm(instance=request.user.profile)
    profiles = Profile.objects.filter(user=user)
    context = {
        'profiles': profiles,
        'prof_form': prof_form,
    }
    return render(request, 'profile.html', context)

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

def deleteFlash(response, id):
    if not response.user.is_authenticated:
        return HttpResponseRedirect("/")
    card = get_object_or_404(flashCard, id=id)
    if not (card.deck in response.user.deck.all()):
        return HttpResponseRedirect("/")
    context = {"deck": card.deck}
    card.delete()
    return HttpResponseRedirect("deck-%d" %card.deck.id)
def deckview(response, id):
    if not response.user.is_authenticated:
        return HttpResponseRedirect("/")
    current_deck = get_object_or_404(deck, id=id)
    if not (current_deck in response.user.deck.all()):
        return HttpResponseRedirect("/")
    context= {"deck": current_deck}
    return render(response, "deckview.html", context)

def question(response, id):
    try:
        card = flashCard.objects.get(id=id)
    except flashCard.DoesNotExist:
            card = None
    if not response.user.is_authenticated:
        pass

    elif card.deck in response.user.deck.all():
        return render(response, "question.html", {"card":card, "id":id})
    return render(response, "home.html", {})

def answer(response, id):
    try:
        card = flashCard.objects.get(id=id)
    except flashCard.DoesNotExist:
            card = None
    if not response.user.is_authenticated:
        pass

    elif card.deck in response.user.deck.all():
        deck = card.deck
        nextcard = flashCard.objects.filter(deck = deck, id__gt=id).first()
        if nextcard:
            nextlink = "/question-" + str(nextcard.id)
            last = False
        else:
            nextlink = "/"
            last = True

        return render(response, "answer.html", {"card":card, "id":id, "nextlink": nextlink, "last": last })
    return render(response, "home.html", {})

class flashCardList(APIView):
    permission_classes = (IsAdminOrReadOnly,)  
    def get_object(self, pk):
        try:
            return flashCard.objects.get(pk=pk)
        except flashCard.DoesNotExist:
            raise Http404

    def get(self, request,pk, format=None):
        all_cards = self.get_object(pk)
        serializers = flashCardSerializer(all_cards)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = flashCardSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)  

    def put(self, request, pk, format=None):
        all_cards = self.get_object(pk)
        serializer = flashCardSerializer(all_cards, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        all_cards = self.get_object(pk)
        all_cards.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
   

class ProfileList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 
    permission_classes = (IsAdminOrReadOnly,)
class DeckList(APIView):
    def get(self, request, format=None):
        all_decks = deck.objects.all()
        serializers = DeckSerializer(all_decks, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = DeckSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    permission_classes = (IsAdminOrReadOnly,)


class ProfileDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_profile(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        merch = self.get_profile(pk)
        serializers = ProfileSerializer(merch)
        return Response(serializers.data)











