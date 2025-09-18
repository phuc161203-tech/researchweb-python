from django.contrib import admin
from blogScience.models import blogCategory, saleProduct, pdfArticle, courseCategory
from blogScience.models import newContactForm, coContactForm, courseContactForm, ShopContact, articleContactForm
from .models import BaiBao, Subscriber, PendingArticle

# Register your models here.
admin.site.register(blogCategory)
admin.site.register(saleProduct)
admin.site.register(pdfArticle)
admin.site.register(courseCategory)

admin.site.register(newContactForm)
admin.site.register(courseContactForm)
admin.site.register(ShopContact)
admin.site.register(articleContactForm)
admin.site.register(coContactForm)

admin.site.register(BaiBao)
admin.site.register(Subscriber)
admin.site.register(PendingArticle)







