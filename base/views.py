from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from django.http import HttpResponse
 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
# Create your views here.

 


def home(request): 
    q = request.GET.get('q')
    all_rooms = Room.objects.all()
    rooms=None
    if q != None:
        # messages_feeds = Message.objects.filter(Q(body__icontains=q)).values_list('room')
        messages_feeds = Message.objects.filter(Q(body__icontains=q)).values_list('room', flat=True).distinct()
        print(messages_feeds)
        rooms_algorithm1 = Room.objects.filter(id__in=messages_feeds)

        # rooms_algorithm1=None
        # print(messages_feeds)
        # for room in range(len(messages_feeds)):
        #     if room:
        #         rooms_algorithm1= Room.objects.filter(id=room[0])
                
        rooms_algorithm2 = Room.objects.filter(Q(topic__name__icontains=q)
                                    |Q(name__icontains=q)
                                    |Q(description__icontains=q))
        if rooms_algorithm2 is not None and rooms_algorithm1 is not None:
            print("Union")
            rooms= list(rooms_algorithm1.union(rooms_algorithm2))
        else:   
            rooms = rooms_algorithm2                                
    elif q ==None:
        rooms = Room.objects.all()
        # for room in rooms: 
    topics = Topic.objects.all()
    topics_dict={} 
    topics_list=[]
    single_dict={}
    length_list=[]
    topic_list=[]
    for topic in topics:
        rooms_2 = Room.objects.filter(topic__name=topic)
        # for room in rooms:
        # print(topic,q)
        topics_dict[topic.name]=len(rooms_2)

        topic_list.append(topic.name)
        length_list.append(len(rooms_2))
        topics_list= [{'length':length_list[i],'name':topic_list[i]} for i in range(len(topic_list))]
    
    length= len(all_rooms)
    q2 = q
    q3=q
    if q==None:
        q2='All'
        q3=''
    feeds_list=[]    
    room_ids = Room.objects.filter(Q(topic__name__icontains=q3)
                                    |Q(name__icontains=q3)
                                    |Q(description__icontains=q3)).values_list('id',flat=True)
    
    feeds_algorithm = Message.objects.filter(room_id__in=room_ids)
    feeds2_algorithm = Message.objects.filter(Q(room__topic__name__icontains=q3)
                                   |Q(body__icontains=q3))


    feeds= list(feeds_algorithm.union(feeds2_algorithm))
    for feed in feeds:
        room = Room.objects.get(name=feed.room)
        room_id = room.id
        feeds_list.append({'room_id':room_id,'feed':feed})
    context = {
        'rooms':rooms,
        'topics':topics_list, 
        'all_rooms':len(all_rooms),
        'q':q2,
        'room_count':len(rooms),
        'feeds_list':feeds_list
        }
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all().order_by('-created')
    participants = []
    for message in messages:
        participants.append(message.user)
    #remove duplicates from list    
    participants = list(dict.fromkeys(participants))
    if request.method == 'POST':
        message= Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        return redirect('room', pk=room.id )
    context = {'room':room, 'messages':messages, 'participants':participants}
    print(messages)
    return render(request,'base/room.html',context)



@login_required(login_url='auth')
def createRoom(request):
    
    form = RoomForm
    topics = Topic.objects.all()
    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        print(request.POST)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        

        # form=RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host= request.user
        #     room.save()
        return redirect('home')
    context={'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context )

@login_required(login_url='auth')
def updateRoom(request, pk):
        
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form=RoomForm(instance=room)
    print(room)
    if request.user != room.host:
         return HttpResponse('You are not allowed')

    if request.method == 'POST':
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('home')

    context={'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context )

@login_required(login_url='auth')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})



def user_auth(request):
    page = 'login'
    message="" 
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email)
        try: 
            print("in try block")
            user=User.objects.get(email=email)
            print("fetching user...")
        except:
            message="User does not exist"
            context={'message':message, 'page':page}
            return render(request, 'base/auth.html', context)        
        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            message="Invalid Credentials"

    context={'message':message, 'page':page}
    return render(request, 'base/auth.html', context)

def log_out(request):
    logout(request)
    return redirect('home')


def user_register(request): 
    form = MyUserCreationForm()
    message = ""
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            message= "Error occured during registration"
    page='register'
    context={'form':form, 'message':message}
    return render(request,'base/auth.html',context)



@login_required(login_url='auth')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})


def userProfile(request,pk):
    user= User.objects.get(id=pk)
    rooms=user.room_set.all()
    user_rooms = Room.objects.filter(host=user.id)
    topics = Topic.objects.all()
    feeds=Message.objects.filter(user=user.id)
    print(feeds)
    context={'user':user,'rooms':rooms, 'topics':topics, 'feeds':feeds}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        print(request.user)
        form = UserForm(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            print(form)
            form.save()
            return redirect('profile', pk=user.id )

    return render(request, 'base/update-user.html',{'form':form})