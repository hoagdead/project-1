from django.db import models
from django.contrib.auth.models import User

"""
 khi tạo room nó sẽ gửi nhưng thông tin này về database
 model mẫu
 class -tên model- (models.Model):
    -model đó sẽ có gì-
    -giải thích hàm: 
        + models.ForeignKey:áp dụng các model khác cho model này
        + models.Charfield: lấy ký tự (ít)
        + models.TextField: lấy ký tự (nhiều)
        + models.DateTimeField: lấy thời gian (ngày-tháng-năm)
        + models.ImageField: lấy hình ảnh
"""

#khỏi tạo một topic mới
class Topic(models.Model):
    #tên của topic
    name = models.CharField(max_length=200)
    #topic đó là gì
    description = models.TextField(null = True, blank = True)
    def __str__ (self):
        return self.name
class Room(models.Model):
    #tên của người tạo ra room đó, khi xóa đi sẽ mất hết, và có thể để trống
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    #topic của room là gì
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null = True)
    #tên của room
    name= models.CharField(max_length=200)
    #room có nội dung là gì
    description = models.TextField(null = True, blank = True)
    #participants = models.ManyToManyField()
    #thời gian tạo, thời gian update
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name   
    class Meta:
        #được sắp xếp theo thứ tự update và created mới nhất
        ordering = ["-updated", "-created"]

#tạo model bình luận
class Message(models.Model):
    #ai gửi bình luận
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #nằm ở room nào
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    #nội dung
    body = models.TextField()
    #thời gian tạo, thời gian update    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    #sẽ cho thấy nội dung tin nhắn trong admin...
    def __str__(self):
        return self.body[:50] + "..." 



"""
    testing
"""
class UserProfile(models.Model):
    user_id=models.CharField(max_length=100, unique=True, primary_key=True)
    user_name = models.CharField(max_length=100)
    user_avata = models.ImageField(blank=True)
    user_background = models.ImageField(blank=True)
    

class Question(models.Model):
    name = models.TextField(max_length=1000,blank=True)
    Ans_a = models.TextField(max_length=1000,blank=True)
    Ans_b = models.TextField(max_length=1000,blank=True)
    Ans_c = models.TextField(max_length=1000,blank=True)
    Ans_d = models.TextField(max_length=1000,blank=True)
    
    SELECTION_CHOICES = [
        ('A', 'Answer A'),
        ('B', 'Answer B'),
        ('C', 'Answer C'),
        ('D', 'Answer D'),
    ]
    

    Corect_ans = models.CharField(max_length=1, choices=SELECTION_CHOICES, default=None)
    type = models.IntegerField(default=1,editable=False)
    def __str__(self):
        return self.name

    