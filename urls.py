from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import course_list
from app_customer import views as customer_views
from .views import arxiv_pdf_proxy

app_name = 'blogScience'

urlpatterns = [
    path('admin/', admin.site.urls),

    # CV/Personal
    path('cv/', views.CV, name='cv'),

    # SALE/COURSE (giữ nguyên các phần khác)
    path('sale-404/', views.course_404, name='sale-404'),
    path('sale-about/', views.course_about, name='sale-about'),
    path('sale-contact/', views.course_contact, name='sale-contact'),
    path('sale-courses/', views.course_courses, name='sale-courses'),
    path('sale-courses/<int:pk>/', views.course_about, name='sale-course-about'),
    path('sale-index/', views.course_index, name='sale-index'),
    path('sale-team/', views.course_team, name='sale-team'),
    path('sale-testimonial/', views.course_testimonial, name='sale-testimonial'),
    path('sale-base/', views.course_base, name='sale-base'),
    path('courses/', course_list, name='course-list'),


    # --------- NEWS (Tin tức, hoàn toàn tách biệt) ---------
       # Tin tức (New)
    path('news/', views.new_index, name='new-index'),
    path('news/<int:pk>/', views.new_details, name='new-details'),


    path('new-about/', views.new_about, name='new-about'),
    path('new-blog/', views.new_blog, name='new-blog'),
    path('new-contact/', views.new_contact, name='new-contact'),
    path('new-categori/', views.new_category, name='new-category'),
    path('new-elements/', views.new_elements, name='new-elements'),
    path('new-latest/', views.new_latest_news, name='new-latest'),
    path('new-main/', views.new_main, name='new-main'),
    path('new-single-blog/', views.new_single_blog, name='new-single-blog'),


    # --------- ARTICLE (Bài báo khoa học, hoàn toàn tách biệt) ---------
    path('article-about/', views.article_about, name='article-about'),
    path('article-blog/', views.article_blog, name='article-blog'),
    path('article-contact/', views.article_contact, name='article-contact'),
    path("article-index/", views.article_index, name="article-index"),
    path('article-service/', views.article_service, name='article-service'),

    # SUBMIT ARTICLE & EVENT REGISTRATION
    path('submit-article/', views.submit_article, name='submit-article'),
    path('review-pending-article/<int:pk>/', views.review_pending_article, name='review-pending-article'),
    path('event-registration/', views.event_registration, name='event-registration'),
    path('event-registration/pdf/<int:reg_id>/', views.event_registration_pdf, name='event_registration_pdf'),
    path('subscribe/', views.subscribe_view, name='subscribe'),



    # BÌNH LUẬN BÀI BÁO (Dùng cho news và article, nhưng ở đây là cho news chi tiết):
    path('news/<int:pk>/comment/', views.submit_comment, name='submit-comment'),

    # SHOP
    path('shop-cart/', views.shop_cart, name='shop-cart'),
    path('shop-checkout/', views.shop_checkout, name='shop-checkout'),
    path('shop-contact/', views.shop_contact, name='shop-contact'),
    path('shop-detail/', views.shop_detail, name='shop-detail'),
    path('shop-index/', views.shop_index, name='shop-index'),
    path('shop-shop/', views.shop_shop, name='shop-shop'),

    # AUTH
    path('log-in-out/', customer_views.dang_nhap, name='log-in-out'),
    path('check-out/', views.check_out, name='check-out'),

    path('ajax-course-register/', views.ajax_course_register, name='ajax-course-register'),
    path('ajax-course-comment/',  views.ajax_course_comment,  name='ajax-course-comment'),
    path(
    'event-registration/preview/<int:reg_id>/',
    views.event_registration_preview,
    name='event_registration_preview'
),

    path('api/stocks', views.stocks_api, name='stocks_api'),
    path('article-blog/approve/<int:pk>/', views.approve_pending_article, name='approve-pending-article'),


    path("proxy/pdf/<str:arxiv_id>.pdf", views.arxiv_pdf_proxy, name="arxiv_pdf_proxy"),

    path('article-blog/<int:pk>/', views.article_blog_details, name='article-blog-details'),
    path('article-blog/<int:pk>/ajax-add-comment/', 
        views.ajax_add_comment, 
        name='ajax-add-comment'),
    path('article-blog/cancel/<int:pk>/', views.cancel_pending_article_confirm, name='cancel-pending-article-confirm'),
    path('article-blog/cancel/<int:pk>/submit/', views.cancel_pending_article, name='cancel-pending-article'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
