from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Authentication: Login, Logout, Register
    path('logout/', views.Logoutuser, name="logout"),
    path('login/', views.Loginpage, name="login"),
    path('register/', views.registerpage, name="register"),

    # Trang chính và các phòng học
    path('forum', views.home, name="forum"),
    path('', views.trang_chu, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createroom, name="create-room"),
    path('update-room/<str:pk>/', views.updateroom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    # Quản lý hồ sơ cá nhân
    path('profile/<str:pk>/', views.userprofile, name="profile"),
    path('profile/update/', views.update_profile, name="update_profile"),

    # Câu hỏi và bài học
    path('create-question/', views.createquestion, name="create-question"),
    path('uploadbaihoc/', views.upload_questions, name='upload_bai_hoc'),
    path('upload_cau_hoi/', views.upload_file, name='upload_questions'),
    path('preview/', views.preview_lesson, name='preview_lesson'),
    path('0n_tap/', views.bai_hoc_all, name='on_tap_pv'),
    path('on_tap/', views.bai_hoc_i, name='on_tap'),
    path('on_tap/bai/<int:lesson_id>/', views.bai, name='bai'),
    path('luyen_tap/', views.luyen_tap_all, name='luyen_tap_all'),
    path('luyen_tap/bai/<int:bai_id>/', views.submit_luyentap, name='luyen_tap'),
    path('luyen_tap/bai/submit/<int:bai_id>/', views.submit_luyentap, name='submit_luyentap'),

    # Thi thử
    path('thi_thu/', views.thi_thu, name='thi_thu'),
    path('thi_thu/de/<int:de_id>/', views.hien_thi_cau_hoi, name='de_thi'),
    path('thi_thu/de/submit/<int:de_id>/', views.nop_dap_an, name='submit_answer'),

    # Quản lý giao diện
    path('change-mode/', views.change_mode, name="change-mode"),
    path('set-theme/', views.set_theme, name='set_theme'),

    # Quản lý không gian cá nhân
    path('personal-space/', TemplateView.as_view(template_name='base/dashboard.html'), name='personal-space'),

    # Nhật ký hoạt động của người dùng
    path('activity-log/', views.user_activity_log, name='user_activity_log'),

    # API tích hợp
    path('api/', include('base.api.urls')),

    # Static files (Media)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
