from django.utils.timezone import now
from .models import UserActivity

class LogUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Lưu thông tin hoạt động của người dùng vào cơ sở dữ liệu
        if request.path not in ('/favicon.ico', '/static/'):  # Loại trừ các đường dẫn không cần thiết
            UserActivity.objects.create(
                path=request.path,
                method=request.method,
                timestamp=now(),
                user=request.user if request.user.is_authenticated else None
            )

        return response
