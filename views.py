from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils import timezone
import io
import xhtml2pdf
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import BaiBao

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    blogCategory, courseCategory, pdfArticle, saleProduct,
    PendingArticle, Event, EventRegistration
)
from .forms import (
    articleContactForm, courseContactForm, newContactForm, ShopContactForm,
    checkOut, PendingArticleForm, EventRegistrationForm, SubscriberForm
)
from .models import *

from django.shortcuts import render, get_object_or_404, redirect
from .models import BaiBao, Comment  # Sử dụng đúng model cho bảng "baibao"
from .forms import ArticleCommentForm

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import saleProduct  # model khóa học

from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import pdfArticle
from .forms import PendingArticleForm

from django.conf import settings
from django.urls import reverse

# ------------------ ACCOUNT & LOG ------------------ #
def log_in_out(request):
    """Đăng nhập / Đăng xuất"""
    return render(request, 'accountReg/logInOut.html', {
        'blogcategories': blogCategory.objects.all(),
        'coursecategories': courseCategory.objects.all(),
    })

# ------------------ SUBSCRIPTION (Đăng ký nhận tin) ------------------ #

from django.shortcuts import render
from django.http import JsonResponse
from .forms import SubscriberForm

from .forms import SubscriberForm
from django.http import JsonResponse



from django.db import IntegrityError
from django.utils import timezone
from django.http import JsonResponse

def subscribe_view(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                # Thử tạo mới, nếu đã có thì IntegrityError
                subscriber = Subscriber.objects.create(
                    name=data['name'],
                    email=data['email'],
                    sent_date=timezone.now()
                )
                created = True
            except IntegrityError:
                # Lấy đối tượng đã tồn tại, cập nhật sent_date nếu muốn
                subscriber = Subscriber.objects.get(email=data['email'])
                subscriber.name = data['name']
                subscriber.sent_date = timezone.now()
                subscriber.save()
                created = False

            # Gửi email (console hoặc SMTP tuỳ config)
            subject = "Xác nhận đăng ký nhận thông tin"
            html = render_to_string(
                'articleDetail/subscribe_email.html',
                {'subscriber': subscriber}
            )
            mail = EmailMessage(
                subject, html,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email]
            )
            mail.content_subtype = "html"
            try:
                num = mail.send()
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Lỗi khi gửi email: {e}'
                }, status=500)

            msg = 'Đăng ký thành công! Email xác nhận đã được gửi.'
            if not created:
                msg = 'Bạn đã đăng ký trước đó. Email xác nhận đã được gửi lại.'
            return JsonResponse({'success': True, 'message': msg})

        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # GET: trả về modal content
    form = SubscriberForm()
    return render(request, 'articleDetail/subscribe_modal_content.html', {
        'form': form
    })

# ------------------ ARTICLE BLOG ------------------ #
def article_blog(request):
    """
    Trang danh sách bài báo khoa học với phân trang, lọc theo category và từ khóa
    """
    categories = blogCategory.objects.all()
    category_id = request.GET.get('category')
    keyword = request.GET.get('keyword', '').strip()
    per_page = request.GET.get('per_page') or 8
    subscribe = SubscriberForm.objects.all()

    article_list = pdfArticle.objects.all().order_by('articleDate')
    if category_id:
        article_list = article_list.filter(articleCategory__id=category_id)
    if keyword:
        article_list = article_list.filter(
            articleName__icontains=keyword
        ) | article_list.filter(
            articleAuthor__icontains=keyword
        ) | article_list.filter(
            articleSubject__icontains=keyword
        )

    if request.method == 'POST':
            form = SubscriberForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Đăng ký thành công!'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
            form = SubscriberForm()

    paginator = Paginator(article_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

        
    return render(request, 'articleDetail/article-blog.html', {
        'page_obj': page_obj,
        'danh_sach_san_pham_moi': page_obj.object_list,
        'categories': categories,
        'form':form,
        'subscriber_form': SubscriberForm(),
        'subscribe' : subscribe,
    })

from django.shortcuts import get_object_or_404

def event_registration_preview(request, reg_id):
    """
    View để render preview HTML khi đăng ký thành công
    """
    from .models import EventRegistration
    reg = get_object_or_404(EventRegistration, pk=reg_id)
    return render(request, 'event_registration_preview.html', {
        'reg': reg
    })

from .forms import ArticleCommentForm

from .forms import ArticleCommentForm
from .models import pdfArticle, Comment
from .forms import ArticleCommentForm

from .models import pdfArticle, ArticleComment
from .forms import ArticleCommentForm

from django.shortcuts import render, get_object_or_404, redirect
from .forms import ArticleCommentForm
from .models import pdfArticle, ArticleComment, blogCategory

# views.py
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ArticleCommentForm
from .models import pdfArticle, ArticleComment, blogCategory

# views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ArticleCommentForm
from .models import pdfArticle, ArticleComment, blogCategory

from django.http import JsonResponse

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import pdfArticle, ArticleComment, blogCategory
from .forms import ArticleCommentForm

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import pdfArticle, ArticleComment
from .forms import ArticleCommentForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import pdfArticle, ArticleComment
from .forms import ArticleCommentForm

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import pdfArticle, ArticleComment
from .forms import ArticleCommentForm

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from .models import pdfArticle, ArticleComment
from .forms import ArticleCommentForm

def article_blog_details(request, pk):
    """
    View chịu trách nhiệm:
    - GET: Lấy article + comments để render template.
    - POST: Xử lý form bình luận truyền thống (non-AJAX), tạo ArticleComment mới, rồi redirect lại.
    """
    article = get_object_or_404(pdfArticle, pk=pk)

    # Nếu request POST: xử lý lưu comment
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        parent_id = request.POST.get('parent', '').strip()  # hidden field nếu có reply

        errors = {}
        if not name:
            errors['name'] = 'Tên không được để trống.'
        if not email:
            errors['email'] = 'Email không được để trống.'
        if not message:
            errors['message'] = 'Nội dung bình luận không được để trống.'

        if errors:
            # Nếu có lỗi, lấy lại comments và trả template kèm lỗi (hiển thị ở template)
            comments = ArticleComment.objects.filter(
                article=article,
                parent__isnull=True
            ).order_by('-created_at')
            return render(request, 'articleDetail/article-blog-details.html', {
                'article': article,
                'comments': comments,
                'errors': errors,
                'data': {
                    'message': message,
                    'parent': parent_id
                }
            })

        # Nếu không có lỗi, tìm parent (nếu là reply)
        parent_obj = None
        if parent_id:
            try:
                parent_obj = ArticleComment.objects.get(pk=int(parent_id))
            except (ValueError, ArticleComment.DoesNotExist):
                parent_obj = None

        # Tạo comment mới
        ArticleComment.objects.create(
            article=article,
            name=name,
            email=email,
            message=message,
            parent=parent_obj
        )

        # Sau khi lưu, redirect để tránh tình trạng double POST khi reload
        return redirect(reverse('blogScience:article-blog-details', args=[pk]))

    # Nếu request GET: chỉ hiển thị article + comments
    comments = ArticleComment.objects.filter(
        article=article,
        parent__isnull=True
    ).order_by('-created_at')

    return render(request, 'articleDetail/article-blog-details.html', {
        'article': article,
        'comments': comments,
    })


from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import pdfArticle, Comment  # Giả sử bạn có hai model Article và Comment
from .forms import ArticleCommentForm       # Giả sử bạn có form để xử lý dữ liệu comment

@require_POST

def ajax_add_comment(request, pk):
    """
    Xử lý AJAX POST để thêm comment cho article có id = pk.
    Trả về JSON: { success: True/False, comment: {...} (nếu thành công), errors: {...} (nếu lỗi) }
    """
    # 1. Lấy article dựa vào pk (đường dẫn URL: article-blog/<pk>/ajax-add-comment/)
    article = get_object_or_404(pdfArticle, pk=pk)

    # 2. Đọc các trường POST. Template/JS ta sẽ gửi:
    #    - name       (tên người bình luận)
    #    - email      (email người bình luận)
    #    - message    (nội dung comment)
    #    - parent     (nếu là reply, parent chứa id của comment cha; nếu không thì None)
    name    = request.POST.get('name', '').strip()
    email   = request.POST.get('email', '').strip()
    message = request.POST.get('message', '').strip()
    parent_id = request.POST.get('parent', '').strip()

    errors = {}
    if not name:
        errors['name'] = ['Tên không được để trống.']
    if not email:
        errors['email'] = ['Email không được để trống.']
    if not message:
        errors['message'] = ['Nội dung bình luận không được để trống.']

    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    # 3. Nếu parent_id có giá trị, thử tìm comment cha
    parent_obj = None
    if parent_id:
        try:
            parent_obj = ArticleComment.objects.get(pk=int(parent_id))
        except (ValueError, ArticleComment.DoesNotExist):
            parent_obj = None

    # 4. Tạo mới ArticleComment
    comment = ArticleComment.objects.create(
        article=article,
        name=name,
        email=email,
        message=message,
        parent=parent_obj
    )

    # 5. Chuẩn bị dữ liệu để trả về cho JavaScript (ví dụ: khi append vào DOM)
    #    Bạn có thể trả JSON nhiều hoặc ít trường tuỳ ý. Ở đây ta trả:
    #    id, name, email, message, created_at (định dạng là string), parent (nếu có)
    comment_data = {
        'id': comment.pk,
        'name': comment.name,
        'email': comment.email,
        'message': comment.message,
        'created_at': comment.created_at.strftime('%d/%m/%Y %H:%M'),
        'parent': parent_obj.pk if parent_obj else None,
    }

    return JsonResponse({'success': True, 'comment': comment_data})
# ------------------ ARTICLE SUBMISSION & REVIEW ------------------ #
# views.py

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def submit_article(request):
    """
    Đăng ký nộp bài báo mới (AJAX hoặc form submit bình thường).
    """
    def is_ajax(req):
        return req.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = PendingArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author_user = request.user
            article.status = 'pending'
            article.save()
            # --- gửi email xác nhận nộp bài báo ---
            detail_url = request.build_absolute_uri(
                reverse('blogScience:article-blog-details', args=[article.pk])
            )
            subject = "Xác nhận nộp bài báo khoa học"
            html_content = render_to_string(
                'articleDetail/submit_article_email.html',
                {
                    'article': article,
                    'user': request.user,
                    'detail_url': detail_url
                }
            )
            mail = EmailMessage(
                subject,
                html_content,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email]
            )
            mail.content_subtype = "html"
            mail.send()
            if is_ajax(request):
                return JsonResponse({'success': True, 'pk': article.pk})
            messages.success(request,
                'Bài báo đã được gửi và đang chờ duyệt. Email xác nhận đã được gửi đến bạn.'
            )
            return redirect('blogScience:article-blog')
        else:
            if is_ajax(request):
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PendingArticleForm()

    return render(request, 'articleDetail/submit_article_modal_content.html', {'form': form})


def review_pending_article(request, pk):
    """
    Xem lại bài báo nộp (chỉ xem, không sửa)
    """
    article = get_object_or_404(PendingArticle, pk=pk)
    return render(request, 'articleDetail/review_pending_article_modal.html', {'article': article})

# ------------------ ARTICLE CONTACT ------------------ #


# ------------------ EVENT LIST & REGISTRATION ------------------ #
import csv
from django.conf import settings
import os

def article_about(request):
    events = Event.objects.all().order_by('-datetime')
    categories = blogCategory.objects.all()
    news_featured = BaiBao.objects.order_by('-Ngay_dang')[:6]
    return render(request, 'articleDetail/article-about.html', {
        'events': events,
        'categories': categories,
        'news_featured': news_featured,
    })

# ở đầu file
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  
def event_registration(request):
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            reg = form.save()
            # Sinh URL view PDF
            pdf_url = reverse('blogScience:event_registration_pdf', args=[reg.pk])
            # Trả về luôn preview HTML
            html = render_to_string('event_registration_preview.html', {
                'reg': reg,
                'pdf_url': pdf_url,
            }, request=request)
            return JsonResponse({'success': True, 'html': html})
        else:
            # Lỗi validate, render lại form kèm lỗi
            html = render_to_string('event_registration_modal.html', {
                'form': form
            }, request=request)
            return JsonResponse({'success': False, 'html': html})
    else:
        # GET: chỉ trả form blank với event+date
        event_name = request.GET.get('event', '')
        event_date = request.GET.get('date', '')
        form = EventRegistrationForm(initial={
            'event_name': event_name,
            'event_date': event_date
        })
        return render(request, 'event_registration_modal.html', {
            'form': form
        })


from django.shortcuts import render
from .models import Event  # Đảm bảo import đúng model

def events_timeline(request):
    events = Event.objects.all().order_by('datetime')
    return render(request, 'articleDetail/article-event-timeline.html', {'events': events})



def render_to_pdf(template_src, context_dict):
    """
    Render template HTML thành file PDF (dùng xhtml2pdf)
    """
    from xhtml2pdf import pisa
    html = render_to_string(template_src, context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None



def event_registration_pdf(request, reg_id):
    reg = get_object_or_404(EventRegistration, pk=reg_id)
    html = render_to_string('event_registration_pdf_template.html', {'reg': reg})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="registration.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation failed')
    return response

def send_registration_email(email, pdf_file, registration):
    """
    Gửi email xác nhận đăng ký sự kiện, kèm file PDF
    """
    subject = "Xác nhận đăng ký tham gia sự kiện"
    body = render_to_string('event_registration_email.html', {'reg': registration})
    mail = EmailMessage(subject, body, to=[email])
    if pdf_file:
        mail.attach('registration.pdf', pdf_file, 'application/pdf')
    mail.content_subtype = "html"
    mail.send()

# ------------------ COURSE/SHOP/NEWS (các phần phụ) ------------------ #
# ...Các function dưới giữ nguyên, chú thích rút gọn...

def check_out(request):
    """Trang thanh toán khóa học (dùng cho e-learning/shop)"""
    categories = courseCategory.objects.all()
    form = checkOut(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # TODO: Xử lý gửi mail, lưu database...
        pass
    return render(request, 'shopCourse/checkout-system.html', {
        'categories': categories,
        'form': form,
    })

def CV(request): return render(request, 'blogScience/CV.html')
def course_404(request): return render(request, 'courseSale/course-404.html', {'categories': courseCategory.objects.all(), 'products': saleProduct.objects.all()})
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import saleProduct, CourseRegister, CourseComment, courseCategory
from .forms  import CourseRegisterForm, CourseCommentForm


# ========== TRANG ABOUT MỖI KHÓA HỌC ==========
def course_about(request, pk):
    course      = get_object_or_404(saleProduct, pk=pk)
    categories  = courseCategory.objects.all()

    # --- Xử lý COMMENT phân trang ---
    per_page    = int(request.GET.get('per_page', 5))
    page_num    = request.GET.get('page')
    all_comments = CourseComment.objects.filter(course=course).order_by('-created_at')
    paginator   = Paginator(all_comments, per_page)
    page_obj    = paginator.get_page(page_num)

    per_options = [5, 10, 15, 20, 30, 50, 100]
    return render(request, 'courseSale/course-about.html', {
        'categories': categories,
        'course': course,
        'comments': page_obj.object_list,
        'page_obj': page_obj,
        'per_page': per_page,
        'per_options': per_options,   # ⇦ bổ sung
    })


# ========== AJAX: ĐĂNG KÝ KHÓA HỌC ==========
@csrf_exempt
@require_POST
def ajax_course_register(request):
    """
    Nhận JSON từ modal, validate, lưu bản ghi.
    Trả JSON: {success: bool, error: str}
    """
    import json
    data = json.loads(request.body.decode('utf-8'))
    form = CourseRegisterForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    # form.errors là dict Django → ép thành string cho gọn
    return JsonResponse({'success': False, 'error': str(form.errors)})


# ========== AJAX: BÌNH LUẬN ==========
@csrf_exempt
@require_POST
def ajax_course_comment(request):
    import json
    data = json.loads(request.body.decode('utf-8'))
    course_id = data.get('course_id')

    try:
        course = saleProduct.objects.get(pk=course_id)
    except saleProduct.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Course not found'})

    form = CourseCommentForm(data)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.course = course
        comment.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': str(form.errors)})


# Join now course 
from django.http import JsonResponse
from .models import saleProduct, CourseRegister

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt  # Nếu dùng AJAX cần set up đúng CSRF, hoặc dùng django.middleware.csrf.CsrfViewMiddleware mặc định
@require_POST
def ajax_course_register(request):
    import json
    data = json.loads(request.body.decode('utf-8'))
    # Lấy khóa học
    try:
        course = saleProduct.objects.get(pk=int(data.get('course_id')))
    except saleProduct.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Course not found.'})

    # Validate (có thể bổ sung thêm tuỳ bạn)
    if not data.get('full_name') or not data.get('dob') or not data.get('email') or not data.get('id_card'):
        return JsonResponse({'success': False, 'error': 'Missing required fields.'})

    # Tạo bản ghi
    CourseRegister.objects.create(
        course=course,
        full_name=data.get('full_name'),
        dob=data.get('dob'),
        email=data.get('email'),
        phone=data.get('phone'),
        birth_place=data.get('birth_place'),
        id_card=data.get('id_card'),
        gender=data.get('gender'),
        target=data.get('target'),
        discount_code=data.get('discount_code'),
        note=data.get('note'),
    )
    return JsonResponse({'success': True})


def course_contact(request):
    categories = courseCategory.objects.all()
    form = courseContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Gửi liên hệ thành công!")
        return redirect('blogScience:sale-contact')
    return render(request, 'courseSale/course-contact.html', {'categories': categories, 'form': form})

# ...Tiếp tục các view cho shop, news, article khác như file cũ...

# views.py
from django.shortcuts import render
from .models import saleProduct, courseCategory

def course_list(request):
    # Pull in every saleProduct (with its FK to courseCategory)
    courses    = saleProduct.objects.select_related('courseCategory').all()
    categories = courseCategory.objects.all()

    return render(request, 'course-courses.html', {
        'courses':    courses,
        'categories': categories,
    })
def course_courses(request):
    categories = courseCategory.objects.all()
    per_page = request.GET.get('per_page', 8)
    try:
        per_page = int(per_page)
    except:
        per_page = 8
    page_number = request.GET.get('page')
    courses = saleProduct.objects.select_related('courseCategory').all().order_by('-id')
    paginator = Paginator(courses, per_page)
    page_obj = paginator.get_page(page_number)
    return render(request, 'courseSale/course-courses.html', {
        'categories': categories,
        'page_obj': page_obj,
        'per_page': per_page,
        'per_page_choices': [8, 16, 24, 36, 45, 56, 78, 120],
        'courses':courses,
    })

def course_index(request):

    categories = courseCategory.objects.all()

    return render(request, 'courseSale/course-index.html',{
        'categories': categories,
    })

def course_base(request):
    
    categories = courseCategory.objects.all()

    for category in categories:
        pass

    return render(request, 'courseSale/course-index.html',{
        'categories': categories,
    })

def course_team(request):
    categories = courseCategory.objects.all()

    return render(request, 'courseSale/course-team.html',
                          {'categories': categories,})

def course_testimonial(request):
    categories = courseCategory.objects.all()

    return render(request, 'courseSale/course-testimonial.html',
                          {'categories': categories,})

# news247



def new_about(request):
    return render(request, 'news247/new-about.html') 

def new_blog(request):
    categories = blogCategory.objects.all()

    return render(request, 'news247/new-blog.html',
                  {'categories':categories,}
                  )

def new_category(request):
    categories = blogCategory.objects.all()

    return render(request, 'news247/new-categori.html',
                  {'categories':categories,}
                  )


def new_contact(request):
    if request.method == 'POST':
        form = newContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Có thể thêm thông báo thành công tại đây nếu muốn
            return redirect('new-contact')  # Đổi thành tên url của bạn nếu khác
    else:
        form = newContactForm()

    context = {'form': form}
    return render(request, 'news247/new-contact.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import BaiBao, Comment  # Import đúng model bạn dùng

def new_details(request, pk):
    article = get_object_or_404(BaiBao, pk=pk)
    comments = Comment.objects.filter(article=article).order_by('-created_at')
    related_articles = BaiBao.objects.exclude(pk=pk).order_by('-Ngay_dang')[:5]

    # Lấy 5 bài khác cùng chuyên mục (Ten_bao)
    related_articles = (BaiBao.objects
                            .filter(Ten_bao=article.Ten_bao)
                            .exclude(pk=pk)
                            .order_by('-Ngay_dang')[:5])

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            Comment.objects.create(
                article=article,
                name=name,
                email=email,
                message=message,  # SAI! "content" không phải là field hợp lệ
)

            # Sau khi lưu, redirect lại chính trang chi tiết này
            return redirect('blogScience:new-details', pk=pk)  
            # Đảm bảo 'blogScience:new-details' là name đúng trong urls.py

    return render(request, 'news247/new-details.html', {
        'article': article,
        'comments': comments,
        'related_articles': related_articles,
    })



def new_elements(request):
    categories = blogCategory.objects.all()

    return render(request, 'news247/new-elements.html',
                  {'categories':categories,}
                  )


from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.conf import settings
from .models import BaiBao   # hoặc tên model của bạn

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
import requests                             # ← thêm dòng này
from django.conf import settings            # ← nếu chưa có

from .models import BaiBao
# …

def new_index(request):
    keyword = request.GET.get('keyword', '').strip()
    qs = BaiBao.objects.all()
    if keyword:
        qs = qs.filter(
            Q(Ten_bai_bao__icontains=keyword) |
            Q(Noi_dung_bai_viet__icontains=keyword)
        )
    qs = qs.order_by('-Ngay_dang')
    page_obj = Paginator(qs, 9).get_page(request.GET.get('page'))

    cities = {
        'Hà Nội': 'Hanoi, VN',
        'Hồ Chí Minh': 'Ho Chi Minh City, VN',
        'Đà Nẵng':    'Da Nang, VN',
    }
    weather_data = {}
    for city, q in cities.items():
        resp = requests.get(
            'https://api.openweathermap.org/data/2.5/weather',
            params={
                'q':      q,
                'units':  'metric',
                'lang':   'vi',
                'appid':  settings.OPENWEATHER_API_KEY
            }
        )
        if resp.ok:
            d = resp.json()
            weather_data[city] = {
                'temp': round(d['main']['temp']),
                'desc': d['weather'][0]['description'].capitalize(),
                'icon': d['weather'][0]['icon'],
            }

    return render(request, 'news247/new-index.html', {
        'page_obj':     page_obj,
        'keyword':      keyword,
        'weather_data': weather_data,
    })


def new_latest_news(request):
    categories = blogCategory.objects.all()

    return render(request, 'news247/new-latest_news.html',
                  {'categories':categories,}
                  )

def new_main(request):
    categories = blogCategory.objects.all()

    return render(request, 'news247/new-main.html',
                  {'categories':categories,}
                  )

def new_single_blog(request):
    categories = blogCategory.objects.all()

    return render(request, 'news247/new-single-blog.html',
                  {'categories':categories,}
                  )
# articleDetail


from .models import pdfArticle, blogCategory, BaiBao
from .forms import SubscriberForm

from django.db.models import Q
from django.core.paginator import Paginator
from .models import pdfArticle, blogCategory, BaiBao  # Đảm bảo Article là model có 'status'
from .forms import SubscriberForm

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import pdfArticle, blogCategory, BaiBao, PendingArticle
from .forms import SubscriberForm

def article_blog(request):
    """
    Trang blog bài báo – lọc, tìm kiếm, phân trang, hiển thị bài chờ duyệt và của chính người dùng.
    """
    categories = blogCategory.objects.all()
    category_id = request.GET.get('category')
    keyword = request.GET.get('keyword', '').strip()
    order = request.GET.get('order', 'desc')
    per_page = int(request.GET.get('per_page', 8))
    
    # Lọc và sắp xếp bài viết
    article_list = pdfArticle.objects.all()
    if order == 'asc':
        article_list = article_list.order_by('articleDate')
    else:
        article_list = article_list.order_by('-articleDate')
    
    if category_id:
        article_list = article_list.filter(articleCategory__id=category_id)
    
    if keyword:
        article_list = article_list.filter(
            Q(articleName__icontains=keyword) |
            Q(articleAuthor__icontains=keyword) |
            Q(articleSubject__icontains=keyword)
        )

    # Phân trang
    paginator = Paginator(article_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tin tức nổi bật (BaiBao mới nhất)
    news_featured = BaiBao.objects.order_by('-Ngay_dang')[:6]

    # Bài báo đang chờ duyệt
    pending_articles = PendingArticle.objects.filter(approved=False).order_by('-submitted_at')

    # Bài báo đã duyệt
    articles = pdfArticle.objects.filter(status='approved').order_by('-articleDate')

    # Bài báo người dùng đã nộp
    own_articles = []
    if request.user.is_authenticated:
        own_articles = PendingArticle.objects.filter(author_user=request.user).order_by('-submitted_at')

    return render(request, 'articleDetail/article-blog.html', {
        'categories': categories,
        'page_obj': page_obj,
        'danh_sach_san_pham_moi': page_obj.object_list,
        'subscriber_form': SubscriberForm(),
        'news_featured': news_featured,
        'pending_articles': pending_articles,
        'own_articles': own_articles,
    })



from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_active and user.is_superuser

@staff_member_required
@user_passes_test(is_admin)
def approve_pending_article(request, pk):
    pa = get_object_or_404(PendingArticle, pk=pk, approved=False)
    # Tạo record mới trong pdfArticle
    pdf = pdfArticle.objects.create(
        articleCategory = blogCategory.objects.first(),  # hoặc logic chọn category
        articleName     = pa.articleName,
        articleID       = pa.articleID,
        articleAuthor   = pa.articleAuthor,
        articleDirection= pa.articleDirection,
        articleSubject  = pa.articleSubject,
        articleDate     = timezone.now(),
        articleFolder   = 'pdfs-astro-phy',  # nếu cần
    )
    pa.approved = True
    pa.save()
    messages.success(request, f'"{pa.articleName}" đã được duyệt và cập nhật vào database.')
    return redirect('blogScience:article-blog')




from django.shortcuts import render
from django.core.mail import send_mail
from .forms import articleContactForm
from .models import blogCategory

def article_contact(request): 
    categories = blogCategory.objects.all()
    thong_tin = None

    form = articleContactForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()

        # Lấy dữ liệu đã được làm sạch
        first_name = form.cleaned_data['firstName']
        last_name  = form.cleaned_data['lastName']
        email      = form.cleaned_data['email']
        subject    = form.cleaned_data['subject']
        message    = form.cleaned_data['message']

        # Gửi mail (tuỳ chỉnh lại from_email cho phù hợp cấu hình)
        full_message = f"From: {first_name} {last_name} <{email}>\n\n{message}"
        send_mail(
            subject=subject,
            message=full_message,
            from_email=email,
            recipient_list=['hoangphuc161203vn@gmail.com'],
            fail_silently=False,
        )
        thong_tin = '<div>Gửi thông tin thành công!</div>'
        form = articleContactForm()   # Reset lại form sau khi submit

    return render(request, 'articleDetail/article-contact.html',
                  {
                      'categories': categories,
                      'form': form,
                      'thong_tin': thong_tin,   # Đúng key!
                  }
    )


def article_index(request):
    categories = blogCategory.objects.all()
    featured_articles = BaiBao.objects.order_by('-Ngay_dang')[:6]   # Lấy 6 bài mới nhất
    return render(request, 'articleDetail/article-index.html', {
        'categories': categories,
        'featured_articles': featured_articles,
    })



@csrf_exempt  # (nếu test với ajax đơn giản, còn khi dùng {% csrf_token %} thì bỏ dòng này đi)
def submit_comment(request, pk):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Xử lý lưu bình luận, ví dụ:
        from .models import BaiBao, Comment
        article = BaiBao.objects.get(pk=pk)
        Comment.objects.create(article=article, name=name, email=email, message=message)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})



def article_service(request):
    categories = blogCategory.objects.all()

    return render(request, 'articleDetail/article-service.html',
                  {'categories':categories,}
                  )

# shopCourse

def shop_cart(request):
    categories = courseCategory.objects.all()

    return render(request, 'shopCourse/shop-cart.html',
                  {'categories':categories,}
                  )

def shop_checkout(request):
    categories = courseCategory.objects.all()

    return render(request, 'shopCourse/shop-checkout.html',
                  {'categories':categories,}
                  )

def shop_contact(request):
    categories = courseCategory.objects.all()
    form = ShopContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # ... các thao tác khác ...
            return redirect('blogScience:shop-contact')
        else:
            print(form.errors)
    return render(request, 'shopCourse/shop-contact.html', {
        'categories': categories,
        'form': form,
    })

def shop_detail(request):
    categories = courseCategory.objects.all()

    return render(request, 'shopCourse/shop-detail.html',
                  {'categories':categories,}
                  )

def shop_index(request):
    categories = courseCategory.objects.all()

    return render(request, 'shopCourse/shop-index.html',
                  {'categories':categories,}
                  )

def shop_shop(request):
    categories = courseCategory.objects.all()

    return render(request, 'shopCourse/shop-shop.html',
                  {'categories':categories,}
                  )

# views.py
# views.py
from .models import saleProduct, CourseComment

@csrf_exempt
def ajax_course_comment(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        content = data.get('content')
        course_id = data.get('course_id')
        if not (name and email and content and course_id):
            return JsonResponse({'success': False, 'error': 'Thiếu thông tin'})
        try:
            course = saleProduct.objects.get(pk=course_id)
            CourseComment.objects.create(
                course=course,
                name=name,
                email=email,
                content=content
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Phương thức không hợp lệ'})


# views.py
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def stocks_api(request):
    symbols = request.GET.get('symbols', '')
    symbol_list = [s.strip().upper() for s in symbols.split(',') if s.strip()]
    results = []

    for sym in symbol_list:
        price = None
        # Ví dụ dùng Yahoo Finance unofficial API
        try:
            r = requests.get(
                'https://query1.finance.yahoo.com/v7/finance/quote',
                params={'symbols': sym},
                timeout=5
            )
            if r.ok:
                data = r.json().get('quoteResponse', {}).get('result')
                if data:
                    price = data[0].get('regularMarketPrice')
        except Exception as e:
            price = None

        results.append({'symbol': sym, 'price': price})

    return JsonResponse(results, safe=False)

# myapp/views.py
import requests
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_GET
from django.utils.cache import patch_response_headers

@require_GET
def arxiv_pdf_proxy(request, arxiv_id):
    """
    Proxy để fetch file PDF từ arxiv.org và trả về cho client.
    URL mẫu: /proxy/pdf/2502.07836.pdf  (trong URLs, arxiv_id = "2502.07836")
    """
    # Tạo URL gốc đến arxiv.org
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    # Gửi request tới arxiv.org
    try:
        r = requests.get(pdf_url, stream=True, timeout=10)
        r.raise_for_status()
    except Exception as e:
        raise Http404(f"Không thể tải PDF từ arxiv.org: {e}")

    # Trả về content của PDF với đúng content_type
    response = HttpResponse(r.content, content_type="application/pdf")
    # Thiết lập header khuyến nghị cache (tuỳ bạn muốn)
    patch_response_headers(response, cache_timeout=60 * 60)  # cache 1 giờ
    # Nếu muốn hiển inline (browser tự embed), bạn có thể thêm:
    # response["Content-Disposition"] = f'inline; filename="{arxiv_id}.pdf"'
    return response

# blogScience/views.py (ở vị trí gần các view liên quan đến PendingArticle)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models import PendingArticle, pdfArticle
from django.contrib import messages
from django.conf import settings

# … đã có submit_article, review_pending_article …

@login_required
def cancel_pending_article_confirm(request, pk):
    """
    Trả về HTML chứa form modal để admin nhập lý do hủy.
    (chỉ mở trong modal qua AJAX)
    """
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Không đủ quyền.'}, status=403)

    article = get_object_or_404(PendingArticle, pk=pk)
    return render(request, 'articleDetail/cancel_pending_article_modal.html', {
        'article': article
    })

@login_required
def cancel_pending_article(request, pk):
    """
    Xử lý POST khi admin xác nhận hủy duyệt:
    - Đọc lý do hủy từ form
    - Cập nhật status của PendingArticle, chuyển về pdfArticle.status='rejected'
    - Gửi email thông báo lý do cho author_user.email
    - Trả JSON hoặc redirect tuỳ request
    """
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Bạn không có quyền.'}, status=403)

    article = get_object_or_404(PendingArticle, pk=pk)
    reason = request.POST.get('reason', '').strip()
    if not reason:
        return JsonResponse({'success': False, 'error': 'Lý do hủy không được để trống.'}, status=400)

    # Cập nhật trạng thái trong bảng PendingArticle (nếu muốn giữ record)
    article.status = 'rejected'
    article.save()

    # Đồng thời, nếu cũng muốn cập nhật pdfArticle (nếu có record song song),
    # tìm bản ghi pdfArticle dựa vào id tương ứng (nếu PendingArticle lưu foreign key):
    try:
        pdf_obj = pdfArticle.objects.get(pk=article.pk)
        pdf_obj.status = 'rejected'
        pdf_obj.save()
    except pdfArticle.DoesNotExist:
        pass

    # Gửi email thông báo cho tác giả
    to_email = article.author_user.email if article.author_user else None
    if to_email:
        subject = f"[Thông báo] Bài báo “{article.articleName}” bị hủy duyệt"
        # Tạo nội dung email từ template
        body = render_to_string('articleDetail/cancel_article_email.html', {
            'article': article,
            'reason': reason,
            'user': article.author_user,
        })
        email_msg = EmailMessage(
            subject=subject,
            body=body,
            to=[to_email],
        )
        email_msg.content_subtype = "html"
        try:
            email_msg.send()
        except Exception as e:
            # Log nếu cần, nhưng vẫn coi là thành công về mặt chức năng
            print("Lỗi gửi email:", e)

    # Nếu request AJAX, trả JSON; nếu không, redirect với thông báo
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    messages.success(request, f'Bài báo “{article.articleName}” đã được hủy duyệt.')
    return redirect('blogScience:article-blog')

