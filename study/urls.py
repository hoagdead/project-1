from django.contrib import admin
from django.urls import path, include

"""
 url của application khác với url tổng nên khi tạo một urls mới thì 
 hãy tạo ở base/urls.py
""" 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))
    
]

