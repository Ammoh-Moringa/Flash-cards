from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns=[
   path('register/', views.registerPage, name= 'register'),
   path('login/', views.loginPage, name= 'loginpage'),
   path('logout/',views.logoutpage,name='logout'),
   path("", views.home, name = "home" ),
   path("home/", views.home, name = "home" ),
   path("createflash-<int:id>", views.createFlash, name = "createFlash" ),
   path("updateflash-<int:id>", views.updateFlash, name = "updateFlash" ),
   path("question-<int:id>", views.question, name = "question" ),
   path("answer-<int:id>", views.answer, name = "answer" ),
   path("deck-<int:id>", views.deckview, name = "deckview" ),
   path("deleteflash-<int:id>", views.deleteFlash, name = "deleteFlash" ),
   path('api/flashCard/<int:pk>/', views.flashCardList.as_view()),
   path('api/flashCard/', views.flashCardList.as_view()),
   path('api/profilelist',views.ProfileList.as_view(),name='profileEndpoint'),
   path('api/deck/', views.DeckList.as_view()),
   path('api-token-auth/', obtain_auth_token),
   path('api/profile/profile-id/(?P<pk>[0-9]+)/',
        views.ProfileDescription.as_view())
   

]

