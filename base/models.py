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
    

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Người dùng thực hiện
    path = models.CharField(max_length=500)  # Đường dẫn truy cập
    method = models.CharField(max_length=10)  # Loại request: GET, POST, etc.
    timestamp = models.DateTimeField(auto_now_add=True)  # Thời gian thực hiện
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Địa chỉ IP
    user_agent = models.TextField(null=True, blank=True)  # Thông tin trình duyệt

    def __str__(self):
        return f"{self.user.username} - {self.path} - {self.timestamp}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/avatars/', blank=True, null=True)
    background = models.ImageField(upload_to='images/backgrounds/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    preferences = models.JSONField(default=dict, blank=True, null=True)  # Lưu trữ theme, cài đặt cá nhân
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.user.username
class Workspace(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="workspace")
    name = models.CharField(max_length=100, default="My Personal Space")

class Block(models.Model):
    BLOCK_TYPES = [
        ('note', 'Note'),
        ('image', 'Image'),
        ('todolist', 'ToDoList'),
    ]
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="blocks",
        default=1  # ID của Workspace mặc định
    )
    type = models.CharField(max_length=20, choices=BLOCK_TYPES)
    content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
"""
    testing
"""
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)