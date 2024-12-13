from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
#path('tên trang/', view.tên của trang trong views, name = "tên ngắn gọn của trang")
urlpatterns = [
    #url cho trang login/logout/register 
    path('logout/', views.Logoutuser, name="logout"),
    path('login/', views.Loginpage, name="login"),
    path('register/', views.registerpage, name="register"),
    
    #url cho page chính và từng room
    path('', views.trang_chu , name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    
    #url khi muốn cập nhật room
    path('create-room/', views.createroom, name="create-room"),
    path('update-room/<str:pk>/', views.updateroom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    
    #testing
    path('profile/<str:pk>', views.userprofile, name="profile"),
    path('create-question/', views.createquestion, name="create-question"),
    path('change-mode', views.change_mode, name="change-mode"),
    path('personal-space/', TemplateView.as_view(template_name='base/dashboard.html'), name='personal-space'),
    path('api/', include('base.api.urls')), 
    

    path('uploadbaihoc', views.upload_file, name='upload_bai_hoc'),
    path('upload_cau_hoi', views.upload_questions, name='upload_questions'),
    path('set-theme/', views.set_theme, name='set_theme'),
    path('thi_thu/', views.thi_thu, name='thi_thu'),
    path('thi_thu/de/<int:de_id>/', views.question_and_submit, name='de_thi'),
    path('thi_thu/de/submit/<int:de_id>', views.question_and_submit, name='submit_answer'),
    path('preview/<int:lesson_id>/', views.preview_lesson, name='preview_lesson'),  
    path('0n_tap', views.bai_hoc_all, name='on_tap_pv'),
    path('on_tap', views.bai_hoc_i, name='on_tap'),
    path('on_tap/bai/<int:lesson_id>/', views.bai, name='bai'),
    path('luyen_tap', views.luyen_tap_all, name='luyen_tap_all'),
    path('luyen_tap/bai/<int:bai_id>', views.submit_luyentap, name='luyen_tap'),
    path('luyen_tap/bai/submit/<int:bai_id>', views.submit_luyentap, name='submit_luyentap'),
    path('forum/', views.home, name='forum'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
