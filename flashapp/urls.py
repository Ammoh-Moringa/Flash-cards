from django.urls import path
from . import views

urlpatterns = [
        path("", views.home, name = "home" ),
        path("home/", views.home, name = "home" ),
        path("createflash-<int:id>", views.createFlash, name = "createFlash" ),
        path("updateflash-<int:id>", views.updateFlash, name = "updateFlash" ),
    ]