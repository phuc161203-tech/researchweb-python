from django import forms
from blogScience.models import ShopContact
from blogScience.models import coContactForm     as CoContactModel
from blogScience.models import courseContactForm     as CourseContactModel
from blogScience.models import articleContactForm    as ArticleContact
from blogScience.models import newContactForm    as NewContactModel
from .models import Subscriber
from .models import PendingArticle
from .models import EventRegistration

from .models import Comment

from .models import ArticleComment



from django import forms
from .models import Subscriber





class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email', 'name']
        
# forms.py


from django import forms
from .models import Comment

# forms.py (sau khi sửa)
from django import forms
from .models import ArticleComment   # ← import model chính xác

# forms.py
from django import forms
from .models import ArticleComment

from django import forms
from .models import ArticleComment

from django import forms
from .models import ArticleComment

from django import forms
from .models import ArticleComment

class ArticleCommentForm(forms.ModelForm):
    # Đảm bảo parent không required (để reply comment không error)
    parent = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ArticleComment
        fields = ['name', 'email', 'message', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Họ tên bạn'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email bạn'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nội dung bình luận',
                'rows': 4
            }),
            # parent đã override ở trên
        }

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if not parent:
            return None
        return parent






from django import forms
from .models import EventRegistration

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = [
            'full_name', 'email', 'work_phone', 'cell_phone', 'job_title', 'company', 'address',
            'website', 'company_desc', 'products', 'booth_type', 'staff_list', 'competitors',
            'company_logo', 'event_name', 'event_date'
        ]
        widgets = {
            # Không set HiddenInput cho full_name!
            'event_name': forms.HiddenInput(),
            'event_date': forms.HiddenInput(),
        }

class PendingArticleForm(forms.ModelForm):
    class Meta:
        model = PendingArticle
        fields = ['articleName', 'articleID', 'articleAuthor', 'articleDirection', 'articleSubject', 'reportFile', 'candidateImage', 'author_user']
        exclude = ['author_user', 'status']

        widgets = {
            'articleName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên bài báo'}),
            'articleID': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mã số bài báo'}),
            'articleAuthor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tác giả'}),
            'articleDirection': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hướng nghiên cứu'}),
            'articleSubject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chuyên ngành'}),
            'reportFile': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'candidateImage': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'author_user': forms.ClearableFileInput(attrs={'class':'form-control', 'placeholder':'ID Tài khoản'}),

        }



class articleContactForm(forms.ModelForm): # Chạy thành công
    firstName = forms.CharField(
        label='First Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'fname',
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    lastName = forms.CharField(
        label='Last Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'lname',
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'id': 'email',
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    subject = forms.CharField(
        label='Subject',
        max_length=225,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'subject',
            'class': 'form-control',
            'placeholder': 'Subject'
        })
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            'id': 'message',
            'class': 'form-control',
            'cols': 30,
            'rows': 5,
            'placeholder': 'Write your notes or questions here...'
        })
    )

    class Meta:
        model = ArticleContact
        exclude = ['sent_date']



class courseContactForm(forms.ModelForm):
    courseContactName = forms.CharField(
        label='First Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'name',
            'class': 'form-control',
            'placeholder': 'Your Name'
        })
    )
    courseContactEmail = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'id': 'email',
            'class': 'form-control',
            'placeholder': 'Your Email'
        })
    )
    courseContactSubject = forms.CharField(
        label='Subject',
        max_length=225,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'subject',
            'class': 'form-control',
            'placeholder': 'Subject'
        })
    )
    courseContactMessage = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            'id': 'message',
            'class': 'form-control',
            'cols': 30,
            'rows': 5,
            'placeholder': 'Write your notes or questions here...'
        })
    )
    class Meta:
        model = CourseContactModel
        exclude = ['sent_date']

# -*- coding: utf-8 -*-
from django import forms
from .models import CourseRegister, CourseComment


class CourseRegisterForm(forms.ModelForm):
    """
    Không render trong template (dùng để validate phía server
    – client đã có modal HTML). Nếu muốn dùng Django render,
    chỉ cần {{ form.as_p }}.
    """
    class Meta:
        model  = CourseRegister
        exclude = ['registered_at']  # tất cả field khác để mặc định


class CourseCommentForm(forms.ModelForm):
    class Meta:
        model  = CourseComment
        fields = ('name', 'email', 'content')
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'form-control'}),
            'email':   forms.EmailInput(attrs={'class': 'form-control'}),
            'content': forms.TextInput(attrs={'class': 'form-control'}),
        }

class newContactForm(forms.ModelForm):
    newContactName = forms.CharField(
        label='First Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'name': 'name',
            'id': 'name',
            'class': 'form-control valid',
            'placeholder': 'Enter your Name',
            'onfocus': 'this.placeholder =' '',
            'onblur': 'this.placeholder = "Enter your name"'
        })
    )
    newContactEmail = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'name': 'email',
            'id': 'email',
            'class': 'form-control valid',
            'placeholder': 'Enter your email',
            'onfocus': 'this.placeholder =' '',
            'onblur': 'this.placeholder = "Enter email address"'
        })
    )
    newContactSubject = forms.CharField(
        label='Subject',
        max_length=225,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'name': 'subject',
            'id': 'subject',
            'class': 'form-control valid',
            'placeholder': 'Enter subject',
            'onfocus': 'this.placeholder =' '',
            'onblur': 'this.placeholder = "Enter subject"'
        })
    )
    newContactMessage = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            'type': 'message',
            'cols': '30',
            'rows': "9",
            'name': 'message',
            'id': 'email',
            'class': 'form-control valid',
            'placeholder': 'Enter message',
            'onfocus': 'this.placeholder =' '',
            'onblur': 'this.placeholder = "Enter message"'
        })
    )

    class Meta:
        model = NewContactModel
        fields = ['newContactName', 'newContactEmail', 'newContactSubject', 'newContactMessage']

        widgets = {
            'newContactName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'newContactEmail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'newContactSubject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'newContactMessage': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}),
        }

class ShopContactForm(forms.ModelForm):
    saleContactName = forms.CharField(
        label='First Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'name',
            'class': 'form-control',
            'placeholder': 'Your Name',
            'required': 'required',
            'data-validation-required-message': 'Please enter your name'
  })
    )
    saleContactEmail = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'id': 'email',
            'class': 'form-control',
            'placeholder': 'Your Email',
            'required': 'required',
            'data-validation-required-message': 'Please enter your email'
  })
    )
    saleContactSubject = forms.CharField(
        label='Subject',
        max_length=225,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'subject',
            'class': 'form-control',
            'placeholder': 'Subject',
            'required': 'required',
            'data-validation-required-message': 'Please enter a subject'
  })
    )
    saleContactMessage = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            'id': 'message',
            'class': 'form-control',
            'rows': '6',
            'placeholder': 'Message',
            'required': 'required',
            'data-validation-required-message': 'Please enter your message'
  })
    )

    class Meta:
        model = ShopContact
        exclude = ['sent_date']

class checkOut(forms.ModelForm):
    coFirstName = forms.CharField(
        label='Tên của bạn là/ First Name:',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Minh Hoàng Phúc',
        })
    )
    coLastName = forms.CharField(
        label='Họ của bạn là/ Last Name:',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'ĐỖ',
        })
    )
    coEmail = forms.EmailField(
        label='Email của bạn là:',
        widget=forms.EmailInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'example@email.com',
            })
    )
    coMobileNo = forms.CharField(
        label='Số điện thoại của bạn/ Mobile No:',
        max_length=225,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': '+84 0767 883 859',
            })
    )
    coAddressLine1 = forms.CharField(
        label='Địa chỉ nhà thứ nhất/ Address Line 1:',
        max_length=225,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': '123 Nguyễn Tư Giản',
            })
    )
    coAddressLine2 = forms.CharField(
        label='Địa chỉ nhà thứ hai/ Address Line 1:',
        max_length=225,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': '123 Nguyễn Tư Giản',
            })
    )
    coCityResident = forms.CharField(
        label='Thành phố bạn ở/ City:',
        max_length=225,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'TP Hồ Chí Minh',
            })
    )
    coDistrictResident = forms.CharField(
        label='Quận bạn ở/ City:',
        max_length=225,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Quận Gò Vấp',
            })
    )
    coZipCode = forms.CharField(
        label='Mã bưu điện/ Zip Code:',
        max_length=225,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': '024-GV006',
            })
    )

    class Meta:
        model = CoContactModel
        exclude = ['sent_date']

from .models import ArticleComment






