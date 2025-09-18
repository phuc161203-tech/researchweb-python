from .models import KhachHang
from django.contrib.auth.models import User

def create_khachhang(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        email = response.get('email')
        first_name = response.get('given_name')
        last_name = response.get('family_name')

    elif backend.name == 'facebook':
        email = response.get('email')
        first_name = response.get('first_name')
        last_name = response.get('last_name')
        
    else:
        return

    # Sinh ten_dang_nhap duy nhất
    username_base = user.username or email.split('@')[0]
    username = username_base
    counter = 1
    while KhachHang.objects.filter(ten_dang_nhap=username).exists():
        username = f"{username_base}_{counter}"
        counter += 1

    if not KhachHang.objects.filter(email=email).exists():
        KhachHang.objects.create(
            ten_dang_nhap=username,
            mat_khau='OAuth2',
            email=email,
            ho=last_name,
            ten=first_name,
        )