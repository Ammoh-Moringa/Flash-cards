from django.urls import path
from . import views

urlpatterns=[
   path('register/', views.registerPage, name= 'register'),
   path('login/', views.loginPage, name= 'loginpage'),
   path('logout/',views.logoutpage,name='logout'),
   path("", views.home, name = "home" ),
   path("home/", views.home, name = "home" ),
   path("createflash-<int:id>", views.createFlash, name = "createFlash" ),
   path("updateflash-<int:id>", views.updateFlash, name = "updateFlash" ),
   path('api/deck/', views.DeckList.as_view())

]
