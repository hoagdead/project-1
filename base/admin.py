from django.contrib import admin

"""
 đăng ký model để quản lý trong admin
 admin.site.register(ten cua model)
"""
from .models import Room, Topic,  Message,Question,Question2,bai_hoc,Workspace,Block, UserProfile
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Question)
admin.site.register(Question2)
admin.site.register(bai_hoc)
admin.site.register(Workspace)
admin.site.register(Block)
admin.site.register(UserProfile)

