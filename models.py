from django.db import models
from django.utils import timezone
from django.db import models



# Create your models here.



class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=128)
    sent_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.email
    
from django import forms




# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class CourseRegister(models.Model):
    """
    Mỗi bản ghi = 1 học viên đăng ký 1 khóa học.
    """
    course         = models.ForeignKey('saleProduct', on_delete=models.CASCADE, related_name='registrations')
    full_name      = models.CharField(max_length=255)
    dob            = models.DateField()
    email          = models.EmailField()
    phone          = models.CharField(max_length=20, blank=True)
    birth_place    = models.CharField(max_length=128, blank=True)
    id_card        = models.CharField(max_length=32)
    gender         = models.CharField(max_length=8, choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')], blank=True)
    target         = models.CharField(max_length=64, blank=True)
    discount_code  = models.CharField(max_length=32, blank=True)
    note           = models.TextField(blank=True)
    registered_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} – {self.course}"


class CourseComment(models.Model):
    """
    Cảm nghĩ / hỏi đáp cho từng khóa học.
    """
    course      = models.ForeignKey('saleProduct', on_delete=models.CASCADE, related_name='comments')
    name        = models.CharField(max_length=255)
    email       = models.EmailField()
    content     = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} – {self.course}"

    


class EventRegistration(models.Model):
    full_name = models.CharField(max_length=255, blank=True)
    pronouns = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    work_phone = models.CharField(max_length=30, blank=True)
    cell_phone = models.CharField(max_length=30, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=200)
    address = models.CharField(max_length=250, blank=True)
    website = models.URLField(blank=True)
    company_desc = models.CharField(max_length=400, blank=True)
    products = models.CharField(max_length=400, blank=True)
    booth_type = models.CharField(
        max_length=32,
        choices=[
            ('in_person', 'In-person booth only'),
            ('virtual', 'Virtual booth only'),
            ('both', 'Virtual & In-person booth'),
        ]
    )
    staff_list = models.TextField(blank=True)
    competitors = models.TextField(blank=True)
    company_logo = models.FileField(upload_to='event_logos/', blank=True, null=True)
    event_name = models.CharField(max_length=300, blank=True, null=True)
    event_date = models.CharField(max_length=30, blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)


# models.py  (chỉ cắt phần liên quan – các model khác giữ nguyên)
class BaiBao(models.Model):
    Ten_bao            = models.CharField(max_length=255)            # Ví dụ: “Thời sự”
    Ten_bai_bao        = models.CharField(max_length=500)
    Ngay_dang          = models.CharField(max_length=100, blank=True, null=True)
    Link_hinh_minh_hoa = models.URLField(max_length=500, blank=True, null=True)
    Noi_dung_bai_viet  = models.TextField()
    Link_bai_bao       = models.URLField(max_length=500, unique=True)

    def __str__(self):
        return f"{self.Ten_bao} – {self.Ten_bai_bao}"

    # ───── Helper property để template dùng thống nhất ─────
    @property
    def image(self):        # dùng cho hero / feature / mid_block
        return self.Link_hinh_minh_hoa or '/static/news247/img/no-img.jpg'

    @property
    def thumb(self):        # dùng cho sidebar “MỚI”
        return self.image

    @property
    def url(self):
        return self.Link_bai_bao

    @property
    def title(self):
        return self.Ten_bai_bao

    @property
    def date(self):
        return self.Ngay_dang

    @property
    def category(self):
        return self.Ten_bao        # hiển thị cạnh tiêu đề

    @property
    def source(self):
        return self.Ten_bao        # <i class="fa fa-user-circle"></i> …

# blogScience/models.py

class Comment(models.Model):
    article = models.ForeignKey(BaiBao, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at}"



    

class blogCategory(models.Model):
    name = models.CharField(max_length=560)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class courseCategory(models.Model):
    name = models.CharField(max_length=560)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    image = models.CharField(max_length=255)
    views = models.IntegerField(default=0)
    price = models.IntegerField(default=0)  # Thêm dòng này
    description = models.TextField(blank=True)  # Thêm dòng này
    
class saleProduct(models.Model):
    courseCategory = models.ForeignKey(courseCategory, on_delete=models.CASCADE)
    courseName = models.CharField(max_length=255)
    courseDescription = models.TextField(null=True, blank=True)
    courseImage = models.ImageField(upload_to='images/products')
    courseDuration = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)  # Thêm dòng này

    def __str__(self):
        return self.courseName

from django.contrib.auth.models import User

class pdfArticle(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Đã hủy duyệt'),    # ← thêm lựa chọn này
    ]
    articleCategory = models.ForeignKey(blogCategory, on_delete=models.CASCADE)
    articleName = models.CharField(max_length=255)
    articleID = models.CharField(max_length=255)
    articleAuthor = models.TextField(null=True, blank=True)
    articleDirection = models.TextField(null=True, blank=True)
    articleSubject = models.TextField(null=True, blank=True)
    articleDate = models.DateTimeField()
    articleFolder = models.CharField(max_length=100,  default="pdfs-astro-phy" )
    status = models.CharField(max_length=20, choices=[('pending', 'Chờ duyệt'), ('approved', 'Đã duyệt')], default='pending')

    author_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # tác giả (User)



    def __str__(self):
        return self.articleName

class ArticleComment(models.Model):
    article = models.ForeignKey(pdfArticle, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

class articleContactForm(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=455)
    message = models.TextField()
    sent_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject

class courseContactForm(models.Model):
    courseContactName = models.CharField(max_length=255)
    courseContactEmail = models.EmailField()
    courseContactSubject = models.CharField(max_length=455)
    courseContactMessage = models.TextField()
    sent_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.courseContactSubject

class newContactForm(models.Model):
    newContactName = models.CharField(max_length=255)
    newContactEmail = models.EmailField()
    newContactSubject = models.CharField(max_length=455)
    newContactMessage = models.TextField()
    sent_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.newContactSubject

class ShopContact(models.Model):
    saleContactName = models.CharField(max_length=255)
    saleContactEmail = models.EmailField()
    saleContactSubject = models.CharField(max_length=455)
    saleContactMessage = models.TextField()
    sent_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.saleContactSubject

class coContactForm(models.Model):
    coFirstName = models.CharField(max_length=255)
    coLastName = models.CharField(max_length=255)
    coEmail = models.EmailField()
    coMobileNo = models.CharField(max_length=455)
    coAddressLine1 = models.TextField()
    coAddressLine2 = models.TextField()
    coCityResident = models.TextField()
    coDistrictResident = models.TextField()
    coZipCode = models.TextField()

    sent_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
       return f"{self.coFirstName} {self.coLastName}"

# models.py
class SaleCourse(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    duration = models.CharField(max_length=50, blank=True)
    # Thêm các trường khác nếu cần

    def __str__(self):
        return self.name

class CourseComment(models.Model):
    course = models.ForeignKey('saleProduct', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.course})"
    

class PendingArticle(models.Model):
    articleName = models.CharField(max_length=255)
    articleID = models.CharField(max_length=100)
    articleAuthor = models.CharField(max_length=255)
    articleDirection = models.CharField(max_length=255)
    articleSubject = models.CharField(max_length=255)
    reportFile = models.FileField(upload_to='pending_articles/reports/')
    candidateImage = models.ImageField(upload_to='pending_articles/candidates/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('pending', 'Chờ duyệt'), ('approved', 'Đã duyệt')], default='pending')
    author_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # tác giả (User)

class PendingArticle(models.Model):
    articleName = models.CharField(max_length=255)
    articleID = models.CharField(max_length=100)
    articleAuthor = models.CharField(max_length=255)
    articleDirection = models.CharField(max_length=255)
    articleSubject = models.CharField(max_length=255)
    reportFile = models.FileField(upload_to='pending_articles/reports/')
    candidateImage = models.ImageField(upload_to='pending_articles/candidates/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('pending', 'Chờ duyệt'), ('approved', 'Đã duyệt')], default='pending')
    author_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # tác giả (User)
