from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Room, Topic, Message,Question
from .form import RoomForm,QuestionForm
from django.shortcuts import redirect
import random

'''
    ở đây sẽ dùng để xử lý request của người dùng
    một views mẫu:
        @login_required(login_url=('login')) -(optional) yêu cầu người dùng phải đăng nhập mới dùng được-
        def -tên của views đó (nên là tên của trang đó)- (request):
            -các giá trị muốn xử lý-
            context={"-các giá trị muốn sử dụng để in ra hay sử lý trong trang đó-" : -tên giá trị-}
            return render(request, 'url của trang', context)
            hoặc
            return redirect('url của trang muốn chuyển về') sử dụng để chuyển người dùng về một trang khác sẵn có
'''


def Loginpage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home') 
        else:
            messages.error(request, 'Username or password is incorrect')  
    context={'page':page}
    return render(request, 'base/login_register.html', context)


def Logoutuser(request):
    logout(request)
    return redirect('home')

def registerpage(request):
    page='register'
    form  = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong')
            
    return render(request, 'base/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        ) 
    
    topics = Topic.objects.all()
    context = {'rooms': rooms , 'topics':topics }
    return render(request, 'base/home.html', context)

def room(request,pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    room_comment = room.message_set.all()
    if request.method == 'POST':
        comment = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('room',pk = room.id)
    
    context = {'room': room,'room_comment':room_comment, 'topics':topics}
    return render(request, 'base/room.html', context)

@login_required(login_url=('login'))
def createroom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)



def updateroom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html', {'obj':room})

@login_required(login_url=('login'))
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html', {'obj':message})

@login_required(login_url=('login'))
def userprofile(request):
    context={}
    return render(request,'profile.html',context)

def createquestion(request):
    form = QuestionForm()
    if request.method=='POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)
    context={'form':form}
    return render(request,'base/question_form.html',context)        

def question_list(request):
    question_limit = 10  # Số lượng câu hỏi muốn lấy
    questions = get_questions(question_limit)  # Gọi hàm đã tạo trước đó

    return render(request, 'question_list.html', {'questions': questions})

def get_questions(total_limit):
    type_1_limit = 3
    type_1_questions = list(Question.objects.filter(type=1))
    if len(type_1_questions) <= type_1_limit:
        selected_type_1_questions = type_1_questions
    else:
        selected_type_1_questions = random.sample(type_1_questions, type_1_limit)
    all_selected_questions = selected_type_1_questions
    return all_selected_questions
    