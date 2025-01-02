from django import forms
from django.forms import ModelForm
from .models import Room, Question, UploadedFile, User,UserProfile,Question2

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="Upload Word File",
        required=True,
        help_text="Chọn một file Word (.doc, .docx) để tải lên."
    )
class UploadQuestionForm(forms.Form):
    file = forms.FileField(
        label="Chọn file Word",
        required=True,
        help_text="Chọn một file Word (.doc, .docx) để tải lên.",
    )
    de = forms.ChoiceField(
        choices=Question2.DE_CHOICES,
        label="Chọn đề",
        required=True,
        help_text="Chọn đề cho các câu hỏi.",
    )
    loai = forms.ChoiceField(
        choices=Question2.LOAI_CHOICES,
        label="Loại câu hỏi",
        required=True,
        help_text="Chọn loại câu hỏi (Chung, ICT, CS).",
    )


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        labels = {
            'name': 'Room Name',
            'description': 'Room Description',
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


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar','background', 'bio']