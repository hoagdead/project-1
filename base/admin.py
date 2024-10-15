from django.contrib import admin

"""
 đăng ký model để quản lý trong admin
 admin.site.register(ten cua model)
"""
from .models import Room, Topic,  Message
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)