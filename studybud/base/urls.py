from os import name
from django.urls import path
from . import views

urlpatterns=[
  

    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),

  # CRUD OPERATIONS ON ROOM
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>',views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>',views.deleteRoom,name='delete-room'),


  #CRUD OPERATION ON MESSAGES
  path('delete-message/<str:pk>',views.deleteMessage,name='delete-message'),
  path('update-message/<str:pk>',views.updateMessage,name="update-message"),

    
     path('login/',views.loginPage,name="login"),
     path('logout/',views.logoutUser,name="logout"),
     path('register/',views.registerPage,name="register")
]