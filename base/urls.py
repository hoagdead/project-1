from django.urls import path
from . import views

#path('tên trang/', view.tên của trang trong views, name = "tên ngắn gọn của trang")
urlpatterns = [
    #url cho trang login/logout/register 
    path('logout/', views.Logoutuser, name="logout"),
    path('login/', views.Loginpage, name="login"),
    path('register/', views.registerpage, name="register"),
    
    #url cho page chính và từng room
    path('', views.home , name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    
    #url khi muốn cập nhật room
    path('create-room/', views.createroom, name="create-room"),
    path('update-room/<str:pk>/', views.updateroom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    
    #testing
    path('profile/', views.userprofile, name="profile"),
    path('create-question/', views.createquestion, name="create-question"),
    
    path('questions/', views.question_list, name='question_list'),
    path('questions/submit', views.submit_answer, name='submit_answer'),
    
    
]
