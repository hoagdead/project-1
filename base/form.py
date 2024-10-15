from django.forms import ModelForm
from .models import Room

#tạo ra 1 form để tạo room bằng cách lấy form mẫu mà django đã cho
class RoomForm(ModelForm): 
    class Meta:
        model = Room
        fields = '__all__'
        