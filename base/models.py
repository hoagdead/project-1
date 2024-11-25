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

    type = models.IntegerField(default=1,editable=False)
    
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

    type = models.IntegerField(default=2,editable=False)
    def __str__(self):
        return self.name[:50] + "..." 


    



"""
    testing
"""
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user_id=models.CharField(max_length=100, unique=True, primary_key=True)
    user_name = models.CharField(max_length=100)
    user_avata = models.ImageField(blank=True)
    user_background = models.ImageField(blank=True)
   