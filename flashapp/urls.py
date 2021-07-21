from django.urls import path
from . import views

urlpatterns=[
   path('register/', views.registerPage, name= 'register'),
   path('login/', views.loginPage, name= 'loginpage'),
   path('logout/',views.logoutpage,name='logout'),
]