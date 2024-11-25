from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Room, Topic, Message,Question,Question2,bai_hoc
from .form import RoomForm,QuestionForm,UploadFileForm
from django.shortcuts import redirect
import random
import os
from docx import Document 
from django.core.files.storage import default_storage
from django.conf import settings
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .form import UploadQuestionForm
from .utils import process_question_file, save_questions_to_db
from django.utils.html import escape
from docx.oxml.ns import qn
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
    context = {'rooms': rooms , 'topics':topics,}
    return render(request, 'base/home.html', context)

def room(request,pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    room_comment = room.message_set.all()
    comment_count = room_comment.count()
    if request.method == 'POST':
        comment = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('room',pk = room.id)
    
    context = {'room': room,'room_comment':room_comment, 'topics':topics,
               'comment_count':comment_count,}
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

def userprofile(request,pk):
    user= User.objects.get(id=pk)
    rooms = user.room_set.all()
    context={'user':user,'rooms':rooms}
    return render(request,'profile.html',context)


@csrf_exempt
def change_mode(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        theme = data.get("theme", "light")
        if theme in ["dark", "light"]:
            request.session["theme"] = theme
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "invalid theme"}, status=400)
    return JsonResponse({"status": "invalid request"}, status=405)

@login_required(login_url=('login'))
def updateprofile(request):
    return render(request)

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


def question_type1(sl):
    so_luong_cau_hoi_1 = sl
    cau_hoi_nhieu_dap_an = list(Question.objects.filter(type=1))
    if len(cau_hoi_nhieu_dap_an) > so_luong_cau_hoi_1:
        cau_hoi_nhieu_dap_an = random.sample(cau_hoi_nhieu_dap_an, so_luong_cau_hoi_1)
    cau_hoi_nhieu_dap_an = list(Question.objects.filter(type=1))
    if len(cau_hoi_nhieu_dap_an) > so_luong_cau_hoi_1:
        cau_hoi_nhieu_dap_an = random.sample(cau_hoi_nhieu_dap_an, so_luong_cau_hoi_1)
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
    return trao_doi_cau_hoi

def question_type2(sl):
    so_luong_cau_hoi_2 = sl

    # Lấy ngẫu nhiên một số câu hỏi từ model Question (loại chọn đáp án)
    

    # Lấy ngẫu nhiên một số câu hỏi từ model Question2 (loại đúng/sai)
    cau_hoi_dung_sai = list(Question2.objects.filter(type=2))
    if len(cau_hoi_dung_sai) > so_luong_cau_hoi_2:
        cau_hoi_dung_sai = random.sample(cau_hoi_dung_sai, so_luong_cau_hoi_2)

    trao_doi_cau_hoi = []

    
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
    return trao_doi_cau_hoi

def question_list(request):
    tong_cau_hoi = 10
    cau_hoi_loai_1 = 8
    cau_hoi_loai_2 = tong_cau_hoi - cau_hoi_loai_1
    type1 = question_type1(cau_hoi_loai_1)
    type2 = question_type2(cau_hoi_loai_2)
    return render(request, 'question_list.html', {'type1':type1 , 'type2': type2})

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




def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            doc = Document(uploaded_file)

            # Nội dung HTML sẽ được tạo ra
            content = ""

            # Duyệt qua các phần tử của tài liệu
            for element in doc.element.body:
                # Nếu là đoạn văn (paragraph)
                if element.tag == qn('w:p'):  # Kiểm tra đoạn văn
                    paragraph = next(p for p in doc.paragraphs if p._element == element)
                    paragraph_html = "<p style='text-indent: 2em;'>"

                    # Xử lý các đoạn văn (runs)
                    for run in paragraph.runs:
                        text = escape(run.text)

                        # Định dạng văn bản
                        if run.bold:
                            text = f"<strong>{text}</strong>"
                        if run.italic:
                            text = f"<em>{text}</em>"
                        if run.underline:
                            text = f"<u>{text}</u>"
                        if run.font.color and run.font.color.rgb:
                            color = run.font.color.rgb
                            text = f"<span style='color: #{color};'>{text}</span>"

                        paragraph_html += text

                    paragraph_html += "</p>"
                    content += paragraph_html

                # Nếu là bảng (table)
                elif element.tag == qn('w:tbl'):  # Kiểm tra bảng
                    table = next(t for t in doc.tables if t._element == element)
                    table_html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"

                    for row in table.rows:
                        table_html += "<tr>"
                        for cell in row.cells:
                            cell_content = ""
                            for paragraph in cell.paragraphs:
                                for run in paragraph.runs:
                                    text = escape(run.text)
                                    if run.bold:
                                        text = f"<strong>{text}</strong>"
                                    if run.italic:
                                        text = f"<em>{text}</em>"
                                    if run.underline:
                                        text = f"<u>{text}</u>"
                                    if run.font.color and run.font.color.rgb:
                                        color = run.font.color.rgb
                                        text = f"<span style='color: #{color};'>{text}</span>"
                                    cell_content += text
                                cell_content += "<br>"
                            table_html += f"<td>{cell_content}</td>"
                        table_html += "</tr>"
                    table_html += "</table>"
                    content += table_html

            # Lưu vào cơ sở dữ liệu
            lesson = bai_hoc.objects.create(
                name=uploaded_file.name,
                noi_dung=content,
                file_di_kem=uploaded_file
            )

            # Chuyển hướng đến trang preview
            return redirect('preview_lesson', lesson_id=lesson.id)
    else:
        form = UploadFileForm()
    return render(request, 'base/upload_file.html', {'form': form})


def preview_lesson(request, lesson_id):
    try:
        lesson = bai_hoc.objects.get(id=lesson_id)
    except bai_hoc.DoesNotExist:
        return HttpResponse("Lesson not found", status=404)

    return render(request, 'base/preview.html', {'lesson': lesson})

@csrf_exempt
def set_theme(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        theme = data.get('theme', 'light')  # Mặc định là 'light'
        request.session['theme'] = theme  # Lưu vào session
        return JsonResponse({'status': 'success'})

def thi_thu(request):
    context={}
    return render(request, "base/thi_thu.html", context)


def bai_hoc_all(request):
    all_lesson  = bai_hoc.objects.all()
    context={'all_lesson': all_lesson}
    return render(request, "base/bai_hoc_all.html",context)

def bai_hoc_i(request):
    all_lesson  = bai_hoc.objects.all()
    context={'all_lesson': all_lesson}
    return render(request, "base/bai_hoc.html",context)

def bai(request,lesson_id):
    all_lesson  = bai_hoc.objects.all()
    lesson = bai_hoc.objects.get(id=lesson_id)
    ten = lesson.name
    noi_dung = lesson.noi_dung
    file_dinh_kem = lesson.file_di_kem
    context = {
        'ten':ten,
        'noi_dung':noi_dung,
        'file':file_dinh_kem,
        'all_lesson': all_lesson,
    }
    return render(request, 'base/bai_hoc_nd.html',context)

def upload_questions(request):
    if request.method == "POST":
        # Nếu là POST từ preview.html (Lưu câu hỏi vào DB)
        if "save_questions" in request.POST:
            questions = request.session.get("questions", [])  # Lấy danh sách câu hỏi từ session
            selected_bai = request.POST.get("bai")  # Lấy bài học từ form

            # Kiểm tra dữ liệu hợp lệ
            if not selected_bai or not questions:
                return render(request, "base/preview.html", {
                    "questions": questions,
                    "all_bai": bai_hoc.objects.all(),
                    "error": "Chưa chọn bài học hoặc không có câu hỏi để lưu."
                })

            for i, question_data in enumerate(questions):
                correct_answer = request.POST.get(f"correct_{i+1}")  # Đáp án đúng
                Question.objects.create(
                    name=question_data["name"],
                    Ans_a=question_data["Ans_a"],
                    Ans_b=question_data["Ans_b"],
                    Ans_c=question_data["Ans_c"],
                    Ans_d=question_data["Ans_d"],
                    Corect_ans=correct_answer,
                    bai_id=selected_bai,  # Gán bài học vào câu hỏi
                )
            return redirect("upload_questions")  # Redirect về trang upload

        # Nếu là POST từ upload_question.html
        else:
            form = UploadQuestionForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES["file"]  # Lấy file được upload
                questions = process_question_file(file)  # Xử lý file để lấy câu hỏi
                request.session["questions"] = questions  # Lưu câu hỏi vào session
                all_bai = bai_hoc.objects.all()  # Lấy danh sách bài học
                return render(request, "base/preview.html", {"questions": questions, "all_bai": all_bai})

    # Nếu là GET (tải trang upload câu hỏi)
    else:
        print("có cc")
        form = UploadQuestionForm()

    return render(request, "base/upload_question.html", {"form": form})

