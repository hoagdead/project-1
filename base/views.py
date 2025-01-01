from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.db.models.functions import ExtractHour
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.files.storage import default_storage
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.html import escape
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Room, Topic, Message, Question, Question2, bai_hoc, 
    UserActivity, Cau_hoi1, Cau_hoi2,UserProfile
)
from .form import (
    RoomForm, QuestionForm, UploadFileForm, EditUser, 
    UploadQuestionForm, 
)
from .utils import process_question_file, save_questions_to_db

from docx import Document
from docx.oxml.ns import qn

import random
import os
import json


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

@staff_member_required
def activiti_log(request):
    # Thống kê tổng số lượt truy cập trang
    total_page_views = UserActivity.objects.count()

    # Thống kê số lượt truy cập theo đường dẫn
    stats_by_path = (
        UserActivity.objects
        .values('path')          
        .annotate(so_luong=Count('id'))  
        .order_by('-so_luong')      
    )

    # Thống kê số lượt truy cập theo giờ
    stats_by_hour = (
        UserActivity.objects
        .annotate(gio=ExtractHour('timestamp'))  
        .values('gio')
        .annotate(so_luong=Count('id'))
        .order_by('gio')  
    )

    # Thống kê số lượt truy cập các trang cụ thể
    so_luot_dang_ky = UserActivity.objects.filter(path='/register/').count()
    so_luot_forum = UserActivity.objects.filter(path='/forum/').count()
    so_luot_on_tap = UserActivity.objects.filter(path='/0n_tap/').count()
    so_luot_luyen_tap = UserActivity.objects.filter(path='/luyen_tap/').count()
    so_luot_thi_thu = UserActivity.objects.filter(path='/thi_thu/').count()

    context = {                   
        'total_page_views': total_page_views,            
        'stats_by_path': stats_by_path,                  
        'stats_by_hour': stats_by_hour,                  
        'so_luot_dang_ky': so_luot_dang_ky,  
        'so_luot_forum': so_luot_forum,                      
        'so_luot_on_tap': so_luot_on_tap,  
        'so_luot_luyen_tap': so_luot_luyen_tap, 
        'so_luot_thi_thu': so_luot_thi_thu, 
    }
    return render(request, 'base/log.html', context)



@staff_member_required  # Chỉ admin mới xem được
def user_activity_log(request):
    activities = UserActivity.objects.all().order_by('-timestamp')[:100]  # Lấy 100 hoạt động gần nhất
    return render(request, 'base/user_activity_log.html', {'activities': activities})
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
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # Tạo hồ sơ người dùng ngay khi đăng ký
            UserProfile.objects.create(user=user)
            # Đăng nhập và chuyển hướng đến trang chỉnh sửa hồ sơ
            login(request, user)
            return redirect('edit-profile', usid=user.id)  # Chuyển hướng tới URL chỉnh sửa
        else:
            messages.error(request, 'Something went wrong')

    return render(request, 'base/login_register.html', {'form': form})

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
    comment_count =room.message_count()
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

def question_type1():
    cau_hoi_nhieu_dap_an = list(Question.objects.filter(type=1))
    trao_doi_cau_hoi = []
    for question in cau_hoi_nhieu_dap_an:
        answers = [
            ('A', question.Ans_a),
            ('B', question.Ans_b),
            ('C', question.Ans_c),
            ('D', question.Ans_d)
        ]
        trao_doi_cau_hoi.append({
            'type': 'multiple_choice',
            'name': question.name,
            'answers': answers,
            'id': question.id,
            'correct_answer': f"Ans_{question.Corect_ans[-1].lower()}"
        })
    return trao_doi_cau_hoi

def question_type2():
    cau_hoi_dung_sai = list(Question2.objects.filter(type__in=[2, 3, 4, 5]))  # Lọc các loại đúng/sai
    trao_doi_cau_hoi = []
    for question in cau_hoi_dung_sai:
        answers = [
            {'label': 'A', 'text': question.Ans_a, 'correct': question.Corect_ans_a},
            {'label': 'B', 'text': question.Ans_b, 'correct': question.Corect_ans_b},
            {'label': 'C', 'text': question.Ans_c, 'correct': question.Corect_ans_c},
            {'label': 'D', 'text': question.Ans_d, 'correct': question.Corect_ans_d},
        ]
        trao_doi_cau_hoi.append({
            'type': 'true_false',
            'name': question.name,
            'id': question.id,
            'answers': answers,
        })
    return trao_doi_cau_hoi

@csrf_protect
def question_list(request, de_id):
    if request.method == 'POST':
        loai_chon = request.POST.get('loai')
        if loai_chon not in ['ICT', 'CS']:
            messages.error(request, 'Lựa chọn loại câu hỏi không hợp lệ.')
            return redirect('de_thi', de_id=de_id)
        
        request.session['loai_chon'] = loai_chon

        # Lấy và xáo trộn câu hỏi loại 1
        cau_hoi_loai1 = list(Cau_hoi1.objects.filter(De=de_id))
        random.shuffle(cau_hoi_loai1)
        cau_hoi_loai1_chon = cau_hoi_loai1

        # Lấy câu hỏi loại 2 chung
        cau_hoi_chung = list(Cau_hoi2.objects.filter(De=de_id, Loai='chung'))
        if len(cau_hoi_chung) >= 2:
            cau_hoi_chung_chon = random.sample(cau_hoi_chung, 2)
        else:
            cau_hoi_chung_chon = cau_hoi_chung

        # Lấy câu hỏi loại 2 theo loại chọn
        cau_hoi_loai_chon = list(Cau_hoi2.objects.filter(De=de_id, Loai=loai_chon))
        if len(cau_hoi_loai_chon) >= 2:
            cau_hoi_loai_chon = random.sample(cau_hoi_loai_chon, 2)
        else:
            cau_hoi_loai_chon = cau_hoi_loai_chon

        # Kết hợp các câu hỏi loại 2
        cau_hoi_loai2 = cau_hoi_chung_chon + cau_hoi_loai_chon

        # Chuyển đổi câu hỏi loại 1 thành dict
        cau_hoi_loai1_serialized = [
            {
                'id': q.id,
                'noi_dung': q.Noi_dung,
                'A': q.A,
                'B': q.B,
                'C': q.C,
                'D': q.D,
                'dap_an_dung': q.Corect_ans,
                'dap_an': [('A', q.A), ('B', q.B), ('C', q.C), ('D', q.D)],
            }
            for q in cau_hoi_loai1_chon
        ]

        # Chuyển đổi câu hỏi loại 2 thành dict
        cau_hoi_loai2_serialized = [
            {
                'id': q.id,
                'noi_dung': q.Noi_dung,
                'loai': q.Loai,
                'dap_an': [
                    {
                        'chu_thich': 'A',
                        'noi_dung': q.A,
                        'dap_an_dung': q.Corect_ans_a == 'True',
                    },
                    {
                        'chu_thich': 'B',
                        'noi_dung': q.B,
                        'dap_an_dung': q.Corect_ans_b == 'True',
                    },
                    {
                        'chu_thich': 'C',
                        'noi_dung': q.C,
                        'dap_an_dung': q.Corect_ans_c == 'True',
                    },
                    {
                        'chu_thich': 'D',
                        'noi_dung': q.D,
                        'dap_an_dung': q.Corect_ans_d == 'True',
                    },
                ]
            }
            for q in cau_hoi_loai2
        ]

        # Lưu câu hỏi vào session
        request.session['type1_questions'] = cau_hoi_loai1_serialized
        request.session['type2_questions'] = cau_hoi_loai2_serialized

        return redirect('de_thi', de_id=de_id)

    elif request.method == 'GET':
        cau_hoi_loai1 = request.session.get('type1_questions')
        cau_hoi_loai2 = request.session.get('type2_questions')
        loai_chon = request.session.get('loai_chon')

        if not cau_hoi_loai1 or not cau_hoi_loai2:
            return render(request, 'question_list.html', {
                'de': de_id,
                'hien_thi_chon_loai': True,
            })
        else:
            return render(request, 'question_list.html', {
                'type1': cau_hoi_loai1,
                'type2': cau_hoi_loai2,
                'de': de_id,
                'loai_chon': loai_chon,
                'hien_thi_chon_loai': False,
            })
    else:
        messages.error(request, 'Phương thức yêu cầu không hợp lệ.')
        return redirect('thi_thu')

@csrf_protect
def submit1(request, de_id):
    if request.method == 'POST':
        cau_hoi_loai1 = request.session.get('type1_questions', [])
        cau_hoi_loai2 = request.session.get('type2_questions', [])
        loai_chon = request.session.get('loai_chon')

        if not cau_hoi_loai1 or not cau_hoi_loai2:
            messages.error(request, 'Không tìm thấy câu hỏi trong phiên làm bài. Vui lòng bắt đầu lại bài thi.')
            return redirect('de_thi', de_id=de_id)

        dap_an_nguoi_dung = request.POST.dict()

        tong_diem = 0
        du_lieu_danh_gia = []

        # Xử lý câu hỏi loại 1
        for q in cau_hoi_loai1:
            q_id = str(q['id'])
            dap_an = dap_an_nguoi_dung.get(q_id)
            dap_an_dung = q['dap_an_dung']
            dung = dap_an == dap_an_dung
            if dung:
                tong_diem += 1
            du_lieu_danh_gia.append({
                'loai': 'chon_dap_an',
                'id': q['id'],
                'noi_dung': q['noi_dung'],
                'dap_an_nguoi_chon': dap_an,
                'dap_an_dung': dap_an_dung,
                'dung': dung,
                'dap_an': q['dap_an'],
            })

        # Xử lý câu hỏi loại 2
        for q in cau_hoi_loai2:
            q_id = str(q['id'])
            noi_dung = q['noi_dung']
            loai = q.get('loai', 'Chưa xác định')
            dap_an = q['dap_an']
            so_dap_an_dung = 0

            for ans in dap_an:
                chu_thich = ans['chu_thich']
                dung = ans['dap_an_dung']
                da_chon = dap_an_nguoi_dung.get(f'{q_id}_{chu_thich}') == 'True'
                if da_chon and dung:
                    so_dap_an_dung += 1

            if so_dap_an_dung == 1:
                diem = 0.1
            elif so_dap_an_dung == 2:
                diem = 0.25
            elif so_dap_an_dung == 3:
                diem = 0.5
            elif so_dap_an_dung == 4:
                diem = 1
            else:
                diem = 0

            tong_diem += diem

            du_lieu_danh_gia.append({
                'loai': 'dung_sai',
                'id': q['id'],
                'noi_dung': noi_dung,
                'loai_cau_hoi': loai,
                'so_dap_an_dung': so_dap_an_dung,
                'diem': diem,
                'dap_an': [
                    {
                        'chu_thich': ans['chu_thich'],
                        'noi_dung': ans['noi_dung'],
                        'dap_an_nguoi_chon': 'Đ' if (dap_an_nguoi_dung.get(f"{q_id}_{ans['chu_thich']}") == 'True') else 'S',
                        'dap_an_dung': 'Đ' if ans['dap_an_dung'] else 'S',
                        'dung': (dap_an_nguoi_dung.get(f"{q_id}_{ans['chu_thich']}") == 'True') == ans['dap_an_dung'],
                    }
                    for ans in dap_an
                ],
            })

        tong_diem = min(tong_diem, 10)

        try:
            del request.session['type1_questions']
            del request.session['type2_questions']
            del request.session['loai_chon']
        except KeyError:
            pass

        return render(request, 'base/nop_dap_an.html', {
            'diem': tong_diem,
            'du_lieu_danh_gia': du_lieu_danh_gia,
        })

    else:
        messages.error(request, 'Phương thức yêu cầu không hợp lệ.')
        return redirect('thi_thu', de_id=de_id)

import random
def question_and_submit(request, de_id):
    if request.method == 'POST':
        user_answers = json.loads(request.POST.get('userAnswers', '{}'))
        total_score = 0
        review_data = []

        # Lấy danh sách câu hỏi
        type1_questions = question_type1()  # Lấy câu hỏi loại 1
        type2_questions = question_type2()  # Lấy câu hỏi đúng/sai

        # Random và giới hạn số lượng câu hỏi
        random.shuffle(type1_questions)
        random.shuffle(type2_questions)

        type1_questions = type1_questions[:24]  # 24 câu loại 1
        type2_questions = type2_questions[:6]  # 6 câu đúng/sai (2 câu mỗi loại)

        # Xử lý câu hỏi loại 1
        for question in type1_questions:
            question_id = str(question['id'])
            selected_answer = user_answers.get(question_id)
            is_correct = selected_answer == question['correct_answer']
            if is_correct:
                total_score += 1
            review_data.append({
                'type': 'multiple_choice',
                'id': question['id'],
                'name': question['name'],
                'selected_answer': selected_answer,
                'correct_answer': question['correct_answer'],
                'is_correct': is_correct,
                'answers': question['answers'],
            })

        # Xử lý câu hỏi đúng/sai
        for question in type2_questions:
            question_id = str(question['id'])
            answer_states = []
            correct_count = 0

            for answer in question['answers']:
                selected_answer = user_answers.get(f'{question_id}_{answer["label"]}')
                is_correct = selected_answer == str(answer['correct'])
                answer_states.append({
                    'label': answer['label'],
                    'text': answer['text'],
                    'selected_answer': selected_answer,
                    'correct_answer': str(answer['correct']),
                    'is_correct': is_correct,
                })
                if is_correct:
                    correct_count += 1

            # Điểm cho câu đúng/sai
            total_score += correct_count * 0.25
            review_data.append({
                'type': 'true_false',
                'id': question['id'],
                'name': question['name'],
                'answers': answer_states,
            })

        total_score = min(total_score, 10)

        return render(request, 'base/submit_answer.html', {
            'score': total_score,
            'review_data': review_data,
        })

    # Nếu GET, hiển thị danh sách câu hỏi
    type1_questions = question_type1()
    type2_questions = question_type2()

    random.shuffle(type1_questions)
    random.shuffle(type2_questions)

    type1_questions = type1_questions[:24]
    type2_questions = type2_questions[:6]  # 6 câu đúng/sai (2 câu mỗi loại)

    return render(request, 'question_list.html', {
        'type1': type1_questions,
        'type2': type2_questions,
        'de': de_id,
    })


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
        # Xử lý yêu cầu POST từ preview.html (Lưu câu hỏi vào DB)
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

            for question_data in questions:
                Question.objects.create(
                    name=question_data["name"],
                    Ans_a=question_data["Ans_a"],
                    Ans_b=question_data["Ans_b"],
                    Ans_c=question_data["Ans_c"],
                    Ans_d=question_data["Ans_d"],
                    Corect_ans=question_data["correct"],  # Lưu đáp án đúng
                    bai_id=selected_bai,  # Gán bài học vào câu hỏi
                )
            request.session.pop("questions", None)  # Xóa session sau khi lưu
            return redirect("upload_questions")  # Redirect về trang upload

        # Xử lý POST từ upload_question.html
        else:
            form = UploadQuestionForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES["file"]  # Lấy file được upload
                questions = process_question_file(file)  # Xử lý file để lấy câu hỏi
                request.session["questions"] = questions  # Lưu câu hỏi vào session
                all_bai = bai_hoc.objects.all()  # Lấy danh sách bài học
                return render(request, "base/preview.html", {
                    "questions": questions, 
                    "all_bai": all_bai
                })
            else:
                return render(request, "base/upload_question.html", {"form": form, "error": "Form không hợp lệ."})

    # Nếu là GET (tải trang upload câu hỏi)
    else:
        form = UploadQuestionForm()

    return render(request, "base/upload_question.html", {"form": form})

def luyen_tap_all(request):
    all_lesson  = bai_hoc.objects.all()
    context ={'al':all_lesson,}
    return render(request, 'base/luyen_tap_all.html', context)

# Lấy câu hỏi ngẫu nhiên cho phần luyện tập
def question_type1s(sl, bai_id):
    so_luong_cau_hoi_1 = sl
    bai = bai_hoc.objects.get(id=bai_id)
    cau_hoi_nhieu_dap_an = list(Question.objects.filter(bai=bai))  # Lọc câu hỏi theo bài học
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
        trao_doi_cau_hoi.append({
            'type': 'multiple_choice',
            'name': question.name,
            'answers': answers,
            'id': question.id,
            'correct_answer': question.Corect_ans 
        })
    return trao_doi_cau_hoi

# View luyện tập

# Xử lý nộp bài thi

def submit_luyentap(request, bai_id):
    questions = question_type1s(24, bai_id) 
    if request.method == 'POST':
        score = 0
        total_questions = len(questions)
        for question in questions:
            print(request.POST.get(f'answer_{question["id"]}'))
            print("dap an:",question['correct_answer'] )
            selected_answer = request.POST.get(f'answer_{question["id"]}')
            selected_answer = "Ans_" + selected_answer.lower() if selected_answer else None
            if selected_answer and selected_answer == question['correct_answer']:
                score += 1.25 
        return render(request, 'base/submit_answer2.html', {
            'score': score,
            'total_questions': total_questions,
        })
    else:
        return render(request, 'base/luyen_tap.html', {
            'type1': questions,
            'bai_id': bai_id,
        })
def trang_chu(request):
    on_tap = bai_hoc.objects.all()[:10]
    context={'on_tap':on_tap}
    return render(request, 'base/trang_chu.html' ,context)

def userProfile(request,pk):
    user= User.objects.get(id=pk)
    profile = UserProfile.objects.get(user=user)
    rooms = user.room_set.all()
    form = EditUser(instance=request.user)
    context={'user':user,'rooms':rooms, 'form':form,'profile':profile,'usid':pk}
    return render(request,'profile.html',context)

@login_required
def update_profile(request, pk):
    # Lấy user dựa trên pk
    user = get_object_or_404(User, id=pk)

def editprofile(request,pk):
    user= User.objects.get(id=pk)
    form = EditUser(instance=request.user)
    return render(request,'base/update_profile.html', {'form':form})
from django.shortcuts import render, redirect
from .models import Cau_hoi1, Cau_hoi2
from docx import Document

def upload_docx(request):
    if request.method == 'POST' and request.FILES['file']:
        question_type = request.POST.get('question_type')  # Lấy loại câu hỏi từ form
        file = request.FILES['file']
        document = Document(file)

        # Lấy tất cả các đoạn văn
        paragraphs = document.paragraphs

        question = None
        answers = {}

        for para in paragraphs:
            text = para.text.strip()

            if text.startswith("Câu "):  # Phát hiện câu hỏi mới
                # Lưu câu hỏi trước đó
                if question and answers:
                    if question_type == 'Cau_hoi1':
                        Cau_hoi1.objects.create(
                            Noi_dung=question,
                            A=answers.get('A', ''),
                            B=answers.get('B', ''),
                            C=answers.get('C', ''),
                            D=answers.get('D', ''),
                        )
                    elif question_type == 'Cau_hoi2':
                        Cau_hoi2.objects.create(
                            Noi_dung=question,
                            A=answers.get('A', ''),
                            B=answers.get('B', ''),
                            C=answers.get('C', ''),
                            D=answers.get('D', ''),
                            Corect_ans_a='True' if 'Đ' in answers.get('A', '') else 'False',
                            Corect_ans_b='True' if 'Đ' in answers.get('B', '') else 'False',
                            Corect_ans_c='True' if 'Đ' in answers.get('C', '') else 'False',
                            Corect_ans_d='True' if 'Đ' in answers.get('D', '') else 'False',
                        )

                # Cập nhật câu hỏi mới
                question = text.split(".", 1)[1].strip()
                answers = {}

            elif text.startswith("A."):
                answers['A'] = text[2:].strip()
            elif text.startswith("B."):
                answers['B'] = text[2:].strip()
            elif text.startswith("C."):
                answers['C'] = text[2:].strip()
            elif text.startswith("D."):
                answers['D'] = text[2:].strip()

        # Lưu câu hỏi cuối cùng
        if question and answers:
            if question_type == 'Cau_hoi1':
                Cau_hoi1.objects.create(
                    Noi_dung=question,
                    A=answers.get('A', ''),
                    B=answers.get('B', ''),
                    C=answers.get('C', ''),
                    D=answers.get('D', ''),
                )
            elif question_type == 'Cau_hoi2':
                Cau_hoi2.objects.create(
                    Noi_dung=question,
                    A=answers.get('A', ''),
                    B=answers.get('B', ''),
                    C=answers.get('C', ''),
                    D=answers.get('D', ''),
                    Corect_ans_a='True' if 'Đ' in answers.get('A', '') else 'False',
                    Corect_ans_b='True' if 'Đ' in answers.get('B', '') else 'False',
                    Corect_ans_c='True' if 'Đ' in answers.get('C', '') else 'False',
                    Corect_ans_d='True' if 'Đ' in answers.get('D', '') else 'False',
                )

        return redirect('previews')  # Chuyển hướng sau khi thành công

    return render(request, 'base/upload_docx.html')


def previews(request):
    # Lấy danh sách các câu hỏi loại 1 và loại 2
    questions1 = Cau_hoi1.objects.all()
    questions2 = Cau_hoi2.objects.all()

    # Lấy danh sách bài học để hiển thị trong dropdown
    all_bai = bai_hoc.objects.all()

    if request.method == 'POST':
        # Lưu câu hỏi vào bài học được chọn
        bai_id = request.POST.get('bai')
        if bai_id and request.POST.get('save_questions'):
            bai = bai_hoc.objects.get(id=bai_id)
            for question in questions1:
                question.bai = bai
                question.save()
            for question in questions2:
                question.bai = bai
                question.save()
            return redirect('success')  # Chuyển hướng sau khi lưu thành công

    return render(request, 'base/previews2.html', {
        'questions1': questions1,
        'questions2': questions2,
        'all_bai': all_bai,
    })
