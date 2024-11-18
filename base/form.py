#tạo ra 1 form để tạo room bằng cách lấy form mẫu mà django đã cho
from django import forms
from django.forms import ModelForm
from .models import Room, Question,UploadedFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('file',)
        
class RoomForm(ModelForm): 
    class Meta:
        model = Room
        fields = '__all__'
        labels = {
            'name': 'Room Name',
            'description': 'Room Description',
        }
        help_texts = {
            'name': 'Enter the name of the room.',
            'description': 'Provide a brief description of the room.',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter room description here'}),
        }

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Room name'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
 
class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields=['name','Ans_a','Ans_b','Ans_c','Ans_d','Corect_ans']