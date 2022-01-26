from email import message
from http.client import HTTPResponse
from multiprocessing import context
from django.shortcuts import render,redirect
from .models import Message, Room,Topic
from .forms import RoomForm,MessageForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponse
from django.contrib.auth.forms import UserCreationForm 
# Create your views here.

# rooms=[
#     {'id':1,'name':'Lets learn Python'},
#      {'id':2,'name':'Design with me'},
#       {'id':3,'name':'Frontend developers'},
# ]

def loginPage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method =="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get("password")

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exists')
        
        user=authenticate(request,username=username,password=password)


        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or Password does not exists')
        

    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page='register'

    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error ocurred during registration')
            return redirect('register')


    form=UserCreationForm(request.POST)
    return render(request,'base/login_register.html',{'form':form})

def home(request):

    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    print(q)
    rooms=Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
    
    )

    topics=Topic.objects.all()
    room_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))

    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    
    # adding participants to a room who messaged
    participants=room.participants.all()

    # message = room,body,user

    # Adding messages to the room
    if request.method=="POST":
        
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)



def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_message=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_message,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    
    if request.method=='POST':
        form=RoomForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
        

    context={'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def updateRoom(request,pk):

    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user!=room.host:
        return HttpResponse('You are not allowed to perform this action!')
        messages.error(request,'Sorry only the room creator can delete a room')
        return redirect('home')

    if request.method=="POST":
        form=RoomForm(request.POST,instance=room)

        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)

    if request.user!=room.host:
        return HttpResponse('You are not allowed to perform this action!')
        messages.error(request,'Sorry only the room creator can delete a room')
        return redirect('home')

    

    if request.method=="POST":
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})


# delete messages from room

def deleteMessage(request,pk):

    message=Message.objects.get(id=pk)

    if request.user!=message.user:
        return HttpResponse("You are not allowed to delete the message")
        messages.error(request,'Sorry the message can be only deleted by the writter!')
        return redirect('room')

    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})

def updateMessage(request,pk):

    message=Message.objects.get(id=pk)
    form=MessageForm(instance=message)

    if request.user!=message.user:
        return HttpResponse('You are not allowed to perform this action!')
        messages.error(request,'Sorry only the room creator can delete a room')
        return redirect('home')
    
    if request.method=='GET':
        return render(request,'base/message_form.html')

    
    if request.method=='POST':
        form=MessageForm(request.POST,instance=message)

        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/message_form.html',context)
