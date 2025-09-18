from django.db.models import Sum
from .models import CartItem

def cart_count(request):
    """
    Trả về tổng số lượng sản phẩm trong giỏ:
    - Nếu đã đăng nhập: đọc từ bảng CartItem
    - Nếu chưa đăng nhập: tính từ session['cart']
    """
    if request.user.is_authenticated:
        agg = CartItem.objects.filter(user=request.user) \
                              .aggregate(total=Sum('quantity'))
        count = agg['total'] or 0
    else:
        sess = request.session.get('cart', {})
        count = sum(sess.values())
    return {'cart_count': count}