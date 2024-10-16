from django.forms import ModelForm
from .models import Room,Question

#tạo ra 1 form để tạo room bằng cách lấy form mẫu mà django đã cho
class RoomForm(ModelForm): 
    class Meta:
        model = Room
        fields = '__all__'
 
 
class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields=['name','Ans_a','Ans_b','Ans_c','Ans_d','Corect_ans']