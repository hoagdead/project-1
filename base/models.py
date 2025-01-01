from django.db import models
from django.contrib.auth.models import User

"""
 datatabase sẽ lưu những gì models có
 model mẫu
 class -tên model- (models.Model):
    -model đó sẽ có gì-
    -giải thích hàm: 
        + models.ForeignKey:áp dụng các model khác cho model này
        + models.Charfield: lấy ký tự (ít)
        + models.TextField: lấy ký tự (nhiều)
        + models.DateTimeField: lấy thời gian (ngày-tháng-năm)
        + models.ImageField: lấy hình ảnh
        + models.FileField: lấy tệp
"""

# một topic sẽ có gì
class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null = True, blank = True)
    def __str__ (self):
        return self.name
    def room_count(self):
        return self.room_set.count()
    
# một room sẽ có gì   
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null = True)
    name= models.CharField(max_length=200)
    description = models.TextField(null = True, blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name   
    class Meta:
        ordering = ["-updated", "-created"]
    def message_count(self):
        return self.message_set.count()

#tạo model bình luận
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField() 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body[:50] + "..." 
    
class bai_hoc(models.Model):
    name = models.CharField(max_length=2000)
    noi_dung = models.TextField()
    file_di_kem = models.FileField(blank=True)
    def __str__(self):
        return self.name
 

class Question(models.Model):
    name = models.TextField(max_length=1000,blank=True)
    Ans_a = models.TextField(max_length=1000,blank=True)
    Ans_b = models.TextField(max_length=1000,blank=True)
    Ans_c = models.TextField(max_length=1000,blank=True)
    Ans_d = models.TextField(max_length=1000,blank=True)
    bai = models.ForeignKey(bai_hoc,on_delete=models.SET_NULL, null = True)

    SELECTION_CHOICES = [
        ('A', 'Answer A'),
        ('B', 'Answer B'),
        ('C', 'Answer C'),
        ('D', 'Answer D'),
    ]
    Corect_ans = models.CharField(max_length=1, choices=SELECTION_CHOICES, default=None)
    type = models.IntegerField(default=1,editable=True)
    
    def __str__(self):
        return self.name[:50] + "..." 

class Question2(models.Model):
    name = models.TextField(max_length=1000,blank=True)
    Ans_a = models.TextField(max_length=1000,blank=True)
    Ans_b = models.TextField(max_length=1000,blank=True)
    Ans_c = models.TextField(max_length=1000,blank=True)
    Ans_d = models.TextField(max_length=1000,blank=True)
    
    SELECTION_CHOICES = [
        ("True","đúng"),
        ("False","Sai")
    ]
    
    Corect_ans_a = models.CharField(max_length=5, choices=SELECTION_CHOICES, default=None)
    Corect_ans_b = models.CharField(max_length=5, choices=SELECTION_CHOICES, default=None)
    Corect_ans_c = models.CharField(max_length=5, choices=SELECTION_CHOICES, default=None)
    Corect_ans_d = models.CharField(max_length=5, choices=SELECTION_CHOICES, default=None)

    type = models.IntegerField(default=2,editable=True)
    def __str__(self):
        return self.name[:50] + "..." 
    

class Cau_hoi1(models.Model):
    Noi_dung = models.TextField(max_length=1000, blank=True)
    A = models.TextField(max_length=1000, blank=True)
    B = models.TextField(max_length=1000, blank=True)
    C = models.TextField(max_length=1000, blank=True)
    D = models.TextField(max_length=1000, blank=True)

    DE_CHOICES = [
        ("1", "Đề 1"),
        ("2", "Đề 2"),
        ("3", "Đề 3"),
        ("4", "Đề 4"),
        ("5", "Đề 5"),
        ("6", "Đề 6"),
    ]

    CORECT_ANS_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    ]

    Corect_ans = models.CharField(
        max_length=1,
        choices=CORECT_ANS_CHOICES,
        default='A',
        verbose_name="Đáp án đúng"
    )
    De = models.CharField(
        max_length=5,
        choices=DE_CHOICES,
        null=True,  # Thêm null=True
        blank=True,  # Thêm blank=True
        verbose_name="Đề"
    )

    def __str__(self):
        return self.Noi_dung[:50] + "..."

class Cau_hoi2(models.Model):
    Noi_dung = models.TextField(max_length=1000, blank=True)
    A = models.TextField(max_length=1000, blank=True)
    B = models.TextField(max_length=1000, blank=True)
    C = models.TextField(max_length=1000, blank=True)
    D = models.TextField(max_length=1000, blank=True)

    DE_CHOICES = [
        ("1", "Đề 1"),
        ("2", "Đề 2"),
        ("3", "Đề 3"),
        ("4", "Đề 4"),
        ("5", "Đề 5"),
        ("6", "Đề 6"),
    ]

    CORRECT_ANS_CHOICES = [
        ("True", "Đúng"),
        ("False", "Sai"),
    ]

    Corect_ans_a = models.CharField(
        max_length=5,
        choices=CORRECT_ANS_CHOICES,
        default='False',
        verbose_name="Đáp án A đúng?"
    )
    Corect_ans_b = models.CharField(
        max_length=5,
        choices=CORRECT_ANS_CHOICES,
        default='False',
        verbose_name="Đáp án B đúng?"
    )
    Corect_ans_c = models.CharField(
        max_length=5,
        choices=CORRECT_ANS_CHOICES,
        default='False',
        verbose_name="Đáp án C đúng?"
    )
    Corect_ans_d = models.CharField(
        max_length=5,
        choices=CORRECT_ANS_CHOICES,
        default='False',
        verbose_name="Đáp án D đúng?"
    )

    LOAI_CHOICES = [
        ("chung", "Chung"),
        ("ICT", "ICT"),
        ("CS", "CS"),
    ]

    Loai = models.CharField(
        max_length=5,
        choices=LOAI_CHOICES,
        default='chung',
        verbose_name="Loại câu hỏi"
    )
    De = models.CharField(
        max_length=5,
        choices=DE_CHOICES,
        null=True,  # Thêm null=True
        blank=True,  # Thêm blank=True
        verbose_name="Đề"
    )

    def __str__(self):
        return self.Noi_dung[:50] + "..."

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)  # Người dùng thực hiện
    path = models.CharField(max_length=500, null=True)  # Đường dẫn truy cập
    method = models.CharField(max_length=10, null=True)  # Loại request: GET, POST, etc.
    timestamp = models.DateTimeField(auto_now_add=True)  # Thời gian thực hiện
    def __str__(self):
        return f"{self.user.username} - {self.path} - {self.timestamp}"
    

"""
    testing
"""
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=30, null=True)
    avata = models.ImageField(blank=True)
    background = models.ImageField(blank=True)
    bio = models.TextField(max_length=1000, blank=True,null=True)
    on_tap_progress =  models.IntegerField(blank=True,null=True)
    thi_thu_progress =  models.IntegerField(blank=True,null=True)
    highest_score = models.IntegerField(blank=True,null=True)
    forum_progress =  models.IntegerField(blank=True,null=True)
    comment_progress =  models.IntegerField(blank=True,null=True)

   
