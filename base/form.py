from django import forms
from django.forms import ModelForm
from .models import Room, Question, UploadedFile, User,UserProfile
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
from django.contrib.auth.forms import UserCreationForm
=======
>>>>>>> 9c219b7234efa93382a44aee7b5a2fd979e26850
>>>>>>> Stashed changes

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
    QUESTION_TYPE_CHOICES = [
        (1, "Chọn 1 đáp án đúng"),
        (2, "Đúng/Sai"),
    ]
    question_type = forms.ChoiceField(
        choices=QUESTION_TYPE_CHOICES,
        label="Loại câu hỏi",
        widget=forms.RadioSelect
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


class EditUser(ModelForm):
    class Meta:
<<<<<<< HEAD
        model = UserProfile
        fields = ['background','avata','name','bio'] 

=======
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
<<<<<<< Updated upstream
        fields = ['avatar','background', 'bio', 'preferences']
=======
        fields = ['avatar','background', 'bio', 'preferences']
>>>>>>> 9c219b7234efa93382a44aee7b5a2fd979e26850
>>>>>>> Stashed changes
