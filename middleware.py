from django.utils import timezone
from .models import ActivityLog


class ActivityLoggingMiddleware:
    """
    Lưu IP + last_activity vào session và ghi log mọi request (trừ static & admin).
    Thêm vào MIDDLEWARE ngay sau AuthenticationMiddleware.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Lưu thông tin session
        ip = request.META.get('REMOTE_ADDR')
        request.session['ip'] = ip
        request.session['last_activity'] = timezone.now().isoformat()
        request.session.setdefault('login_time', timezone.now().isoformat())

        # Bỏ qua static & admin
        if request.path.startswith(('/static', '/admin')):
            return response

        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='REQUEST',
            detail=request.path[:255]
        )
        return response
