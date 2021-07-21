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
<<<<<<< HEAD
   path('api/profilelist',views.ProfileList.as_view(),name='profileEndpoint'),
=======
   path('api/deck/', views.DeckList.as_view())

>>>>>>> 18de43d0b432db371a13b9a1020d02b5f2bf5000
]

