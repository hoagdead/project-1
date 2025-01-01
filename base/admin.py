from django.contrib import admin

"""
 đăng ký model để quản lý trong admin
 admin.site.register(ten cua model)
"""
<<<<<<< Updated upstream
from .models import Room, Topic,  Message,Question,Question2,bai_hoc,Workspace,Block, UserProfile
admin.site.register(Room)
=======
from .models import Room, Topic,  Message,Question,Question2,bai_hoc,Cau_hoi1,Cau_hoi2, UserProfile
>>>>>>> Stashed changes
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Question)
admin.site.register(Question2)
admin.site.register(bai_hoc)
<<<<<<< Updated upstream
admin.site.register(Workspace)
admin.site.register(Block)
admin.site.register(UserProfile)
=======
admin.site.register(Cau_hoi1)
admin.site.register(Cau_hoi2)
admin.site.register(UserProfile)

>>>>>>> Stashed changes

