from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Room, Topic, Message,Question,Question2
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
    tong_so_luong_cau_hoi = 10
    so_luong_cau_hoi_1 = 3
    so_luong_cau_hoi_2 = tong_so_luong_cau_hoi - so_luong_cau_hoi_1

    # Lấy ngẫu nhiên một số câu hỏi từ model Question (loại chọn đáp án)
    cau_hoi_nhieu_dap_an = list(Question.objects.filter(type=1))
    if len(cau_hoi_nhieu_dap_an) > so_luong_cau_hoi_1:
        cau_hoi_nhieu_dap_an = random.sample(cau_hoi_nhieu_dap_an, so_luong_cau_hoi_1)

    # Lấy ngẫu nhiên một số câu hỏi từ model Question2 (loại đúng/sai)
    cau_hoi_dung_sai = list(Question2.objects.filter(type=2))
    if len(cau_hoi_dung_sai) > so_luong_cau_hoi_2:
        cau_hoi_dung_sai = random.sample(cau_hoi_dung_sai, so_luong_cau_hoi_2)

    trao_doi_cau_hoi = []

    for question in cau_hoi_nhieu_dap_an:
        answers = [
            ('A', question.Ans_a),
            ('B', question.Ans_b),
            ('C', question.Ans_c),
            ('D', question.Ans_d)
        ]
        random.shuffle(answers)  # Xáo trộn thứ tự các đáp án
        trao_doi_cau_hoi.append({
            'type': 'multiple_choice',  # Đánh dấu loại câu hỏi
            'name': question.name,
            'answers': answers,
            'id': question.id,
        })

    # Xáo trộn đáp án cho câu hỏi loại đúng/sai
    for question in cau_hoi_dung_sai:
        answers = [
            ('A', question.Ans_a, question.Corect_ans_a),
            ('B', question.Ans_b, question.Corect_ans_b),
            ('C', question.Ans_c, question.Corect_ans_c),
            ('D', question.Ans_d, question.Corect_ans_d)
        ]
        random.shuffle(answers)  # Xáo trộn thứ tự các đáp án
        trao_doi_cau_hoi.append({
            'type': 'true_false',  # Đánh dấu loại câu hỏi
            'name': question.name,
            'answers': answers,
            'id': question.id,
        })
    return render(request, 'question_list.html', {'questions': trao_doi_cau_hoi})

def submit_answer(request):
    if request.method == 'POST':
        total_score = 0

        # Tính điểm cho câu hỏi loại chọn 1 đáp án
        for question in Question.objects.filter(type=1):
            user_answer = request.POST.get(f'answer_{question.id}')
            if user_answer and user_answer == question.Corect_ans:
                total_score += 1  # Mỗi câu hỏi chọn đáp án đúng được 1 điểm

        # Tính điểm cho câu hỏi loại đúng/sai
        for question in Question2.objects.filter(type=2):
            correct_count = 0

            # Kiểm tra từng đáp án đúng/sai
            user_answer_a = request.POST.get(f'answer_A_{question.id}')
            if user_answer_a and user_answer_a == question.Corect_ans_a:
                correct_count += 1

            user_answer_b = request.POST.get(f'answer_B_{question.id}')
            if user_answer_b and user_answer_b == question.Corect_ans_b:
                correct_count += 1

            user_answer_c = request.POST.get(f'answer_C_{question.id}')
            if user_answer_c and user_answer_c == question.Corect_ans_c:
                correct_count += 1

            user_answer_d = request.POST.get(f'answer_D_{question.id}')
            if user_answer_d and user_answer_d == question.Corect_ans_d:
                correct_count += 1

            # Tính điểm cho câu đúng/sai
            if correct_count == 1:
                total_score += 0.1
            elif correct_count == 2:
                total_score += 0.2
            elif correct_count == 3:
                total_score += 0.5
            elif correct_count == 4:
                total_score += 1
                
        if total_score > 10:
            total_score = 10

        # Sau khi tính điểm, chuyển hướng tới trang kết quả
        return render(request, 'base/submit_answer.html', {'score': total_score})
    return redirect('question_list')