from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Room, Topic, Message,Question,Question2,bai_hoc,UserProfile
from .form import RoomForm,QuestionForm,UploadFileForm,UserForm,UserProfileForm
from django.views.decorators.csrf import csrf_protect
import random
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
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import UserActivity
from django.db.models.functions import ExtractHour

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
def user_activity_log(request):
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
    so_luot_forum = UserActivity.objects.filter(path='/forum/').count()
    so_luot_on_tap = UserActivity.objects.filter(path='/0n_tap/').count()
    so_luot_luyen_tap = UserActivity.objects.filter(path='/luyen_tap/').count()
    so_luot_thi_thu = UserActivity.objects.filter(path='/thi_thu/').count()

    context = {                   
        'total_page_views': total_page_views,            
        'stats_by_path': stats_by_path,                  
        'stats_by_hour': stats_by_hour,                  
        'so_luot_forum': so_luot_forum,                      
        'so_luot_on_tap': so_luot_on_tap,  
        'so_luot_luyen_tap': so_luot_luyen_tap, 
        'so_luot_thi_thu': so_luot_thi_thu, 
    }
    return render(request, 'base/user_activity_log.html', context)



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


@csrf_protect
def hien_thi_cau_hoi(request, de_id):
    if request.method == 'POST':
        loai_chon = request.POST.get('loai')
        if loai_chon not in ['ICT', 'CS']:
            messages.error(request, 'Lựa chọn loại câu hỏi không hợp lệ.')
            return redirect('de_thi', de_id=de_id)

        request.session['loai_chon'] = loai_chon

        # Lấy và xáo trộn câu hỏi loại 1 (dạng single choice)
        cau_hoi_loai1 = list(Question2.objects.filter(De=de_id, type=1))
        random.shuffle(cau_hoi_loai1)

        # Lấy câu hỏi loại 2 (dạng multiple choice chung và theo loại)
        cau_hoi_chung = list(Question2.objects.filter(De=de_id, type=2, Loai='chung'))
        cau_hoi_loai_chon = list(Question2.objects.filter(De=de_id, type=2, Loai=loai_chon))

        cau_hoi_chung_chon = random.sample(cau_hoi_chung, min(2, len(cau_hoi_chung)))
        cau_hoi_loai_chon = random.sample(cau_hoi_loai_chon, min(2, len(cau_hoi_loai_chon)))

        cau_hoi_loai2 = cau_hoi_chung_chon + cau_hoi_loai_chon

        # Lưu câu hỏi vào session
        request.session['type1_questions'] = [
            {
                'id': q.id,
                'noi_dung': q.Noi_dung,
                'A': q.A,
                'B': q.B,
                'C': q.C,
                'D': q.D,
                'dap_an_dung': q.Corect_ans_single,
                'dap_an': [('A', q.A), ('B', q.B), ('C', q.C), ('D', q.D)],
            }
            for q in cau_hoi_loai1
        ]

        request.session['type2_questions'] = [
            {
                'id': q.id,
                'noi_dung': q.Noi_dung,
                'loai': q.Loai,
                'dap_an': [
                    {'chu_thich': 'A', 'noi_dung': q.A, 'dap_an_dung': q.Corect_ans_a == 'True'},
                    {'chu_thich': 'B', 'noi_dung': q.B, 'dap_an_dung': q.Corect_ans_b == 'True'},
                    {'chu_thich': 'C', 'noi_dung': q.C, 'dap_an_dung': q.Corect_ans_c == 'True'},
                    {'chu_thich': 'D', 'noi_dung': q.D, 'dap_an_dung': q.Corect_ans_d == 'True'},
                ],
            }
            for q in cau_hoi_loai2
        ]

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
def nop_dap_an(request, de_id):
    if request.method == 'POST':
        cau_hoi_loai1 = request.session.get('type1_questions', [])
        cau_hoi_loai2 = request.session.get('type2_questions', [])

        if not cau_hoi_loai1 or not cau_hoi_loai2:
            messages.error(request, 'Không tìm thấy câu hỏi trong phiên làm bài. Vui lòng bắt đầu lại bài thi.')
            return redirect('de_thi', de_id=de_id)

        dap_an_nguoi_dung = request.POST.dict()
        tong_diem = 0
        du_lieu_danh_gia = []

        # Xử lý câu hỏi loại 1
        for q in cau_hoi_loai1:
            dap_an = dap_an_nguoi_dung.get(str(q['id']))
            dung = dap_an == q['dap_an_dung']
            if dung:
                tong_diem += 1
            du_lieu_danh_gia.append({
                'loai': 'chon_dap_an',
                'id': q['id'],
                'noi_dung': q['noi_dung'],
                'dap_an_nguoi_chon': dap_an,
                'dap_an_dung': q['dap_an_dung'],
                'dung': dung,
                'dap_an': q['dap_an'],
            })

        # Xử lý câu hỏi loại 2
        for q in cau_hoi_loai2:
            so_dap_an_dung = 0
            for ans in q['dap_an']:
                da_chon = dap_an_nguoi_dung.get(f"{q['id']}_{ans['chu_thich']}") == 'True'
                if da_chon and ans['dap_an_dung']:
                    so_dap_an_dung += 1

            diem = {1: 0.1, 2: 0.25, 3: 0.5, 4: 1}.get(so_dap_an_dung, 0)
            tong_diem += diem

            du_lieu_danh_gia.append({
                'loai': 'dung_sai',
                'id': q['id'],
                'noi_dung': q['noi_dung'],
                'loai_cau_hoi': q['loai'],
                'so_dap_an_dung': so_dap_an_dung,
                'diem': diem,
                'dap_an': [
                    {
                        'chu_thich': ans['chu_thich'],
                        'noi_dung': ans['noi_dung'],
                        'dap_an_nguoi_chon': 'Đ' if (dap_an_nguoi_dung.get(f"{q['id']}_{ans['chu_thich']}") == 'True') else 'S',
                        'dap_an_dung': 'Đ' if ans['dap_an_dung'] else 'S',
                        'dung': (dap_an_nguoi_dung.get(f"{q['id']}_{ans['chu_thich']}") == 'True') == ans['dap_an_dung'],
                    }
                    for ans in q['dap_an']
                ],
            })

        tong_diem = min(tong_diem, 10)

        try:
            del request.session['type1_questions']
            del request.session['type2_questions']
            del request.session['loai_chon']
        except KeyError:
            pass

        return render(request, 'base/submit_anwser.html', {
            'diem': tong_diem,
            'du_lieu_danh_gia': du_lieu_danh_gia,
        })

    else:
        messages.error(request, 'Phương thức yêu cầu không hợp lệ.')
        return redirect('thi_thu', de_id=de_id)
def upload_file(request):
    if request.method == 'POST':
        print('ok')
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            doc = Document(uploaded_file)

            questions = []
            current_type = None  # Loại câu hỏi: 1 (trắc nghiệm) hoặc 2 (đúng/sai)
            current_question = None

            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()

                # Xác định loại câu hỏi dựa trên tiêu đề phần
                if text.startswith(("PHẦN 1", "Phần 1")):
                    current_type = 1
                    continue
                elif text.startswith(("PHẦN 2", "Phần 2")):
                    current_type = 2
                    continue

                # Phát hiện câu hỏi mới
                if text.startswith("Câu "):
                    if current_question:
                        questions.append(current_question)
                    current_question = {
                        "Noi_dung": text.split(": ", 1)[1] if ": " in text else "",
                        "A": "",
                        "B": "",
                        "C": "",
                        "D": "",
                        "Corect_ans_single": None,
                        "Corect_ans_a": "None",
                        "Corect_ans_b": "None",
                        "Corect_ans_c": "None",
                        "Corect_ans_d": "None",
                        "Loai": "None",
                        "type": current_type
                    }

                # Xác định nội dung đáp án
                elif text.startswith(("A.", "B.", "C.", "D.")) and current_question:
                    answer_key = text[0]  # Lấy ký tự đầu tiên (A, B, C, D)
                    answer_text = text[2:].strip()  # Lấy nội dung sau dấu "."
                    if answer_key in ["A", "B", "C", "D"]:
                        current_question[answer_key] = answer_text

                        # Đánh dấu đáp án đúng nếu in đậm
                        is_correct = any(run.bold for run in paragraph.runs)
                        if is_correct:
                            correct_field = f"Corect_ans_{answer_key.lower()}"
                            current_question[correct_field] = "True"

            # Thêm câu hỏi cuối cùng nếu còn sót
            if current_question:
                questions.append(current_question)

            # Lưu câu hỏi vào session để xử lý trong preview
            request.session["questions"] = questions
            return redirect("preview_questions")

    else:
        form = UploadFileForm()
        print('not ok')

    return render(request, 'base/upload_file.html', {'form': form})


def preview_questions(request):
    questions = request.session.get("questions", [])
    if request.method == "POST":
        selected_de = request.POST.get("de")
        if not selected_de:
            return render(request, "base/preview.html", {
                "questions": questions,
                "DE_CHOICES": Question2.DE_CHOICES,
                "LOAI_CHOICES": Question2.LOAI_CHOICES,
                "error": "Bạn cần chọn đề trước khi lưu."
            })

        for idx, question in enumerate(questions):
            if question["type"] == 2:  # Câu hỏi đúng/sai
                question["Loai"] = request.POST.get(f"loai_{idx}", "None")

        # Lưu vào cơ sở dữ liệu
        for q in questions:
            Question2.objects.create(
                Noi_dung=q["Noi_dung"],
                A=q["A"],
                B=q["B"],
                C=q["C"],
                D=q["D"],
                Corect_ans_single=q["Corect_ans_single"],
                Corect_ans_a=q["Corect_ans_a"],
                Corect_ans_b=q["Corect_ans_b"],
                Corect_ans_c=q["Corect_ans_c"],
                Corect_ans_d=q["Corect_ans_d"],
                Loai=q["Loai"],
                De=selected_de,
                type=q["type"]
            )

        request.session.pop("questions", None)
        return redirect("upload_bai_hoc")

    return render(request, "base/preview.html", {
        "questions": questions,
        "DE_CHOICES": Question2.DE_CHOICES,
        "LOAI_CHOICES": Question2.LOAI_CHOICES
    })



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
        if "save_questions" in request.POST:
            questions = request.session.get("questions", [])
            selected_de = request.POST.get("de")
            selected_loai = request.POST.get("loai")

            if not selected_de or not selected_loai or not questions:
                return render(request, "base/preview.html", {
                    "questions": questions,
                    "error": "Chưa chọn đầy đủ thông tin hoặc không có câu hỏi để lưu."
                })

            save_questions_to_db(questions, selected_de, selected_loai)
            request.session.pop("questions", None)
            return redirect("upload_questions")

        else:
            form = UploadQuestionForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES["file"]
                de = form.cleaned_data["de"]
                loai = form.cleaned_data["loai"]
                
                try:
                    questions = process_question_file(file)
                except ValueError as e:
                    return render(request, "base/upload_question.html", {"form": form, "error": str(e)})

                request.session["questions"] = questions
                return render(request, "base/preview.html", {"questions": questions, "de": de, "loai": loai})
            else:
                return render(request, "base/upload_question.html", {"form": form, "error": "Form không hợp lệ."})

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

def userprofile(request, pk):
    # Lấy người dùng dựa trên primary key (pk)
    user = get_object_or_404(User, id=pk)
    rooms = Room.objects.filter(host=user)
    user_profile = UserProfile.objects.filter(user=user).first()
    form = UserForm(instance=request.user) if request.user == user else None
    context = {
        'user': user,
        'rooms': rooms,
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)

@login_required
def update_profile(request, pk):
    # Lấy user dựa trên pk
    user = get_object_or_404(User, id=pk)

    if request.user != user:
        return HttpResponse("Bạn không có quyền cập nhật hồ sơ này.", status=403)

    # Lấy hoặc tạo UserProfile
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=pk)  # Quay lại trang hồ sơ cá nhân
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'base/update_profile.html', {'form': form, 'user': user})
#test
