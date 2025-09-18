"""
URL configuration for WebsiteNCKH project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blogScience.views import CV
from blogScience.views import course_404,course_about,course_contact,course_courses,course_index,course_team, course_testimonial
from blogScience.views import new_about, new_blog, new_category,new_contact,new_details,new_elements,new_index,new_latest_news,new_main,new_single_blog
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    # shop app
    path("", include(("app_customer.urls", "app_customer"), namespace="app_customer")),

    # blogScience app
    path("blog/", include(("blogScience.urls", "blogScience"), namespace="blogScience")),

    path("contest/", include(("contestApp.urls", "contestApp"), namespace="contestApp")),
    
    path("work/", include(("app_work.urls", "app_work"), namespace="app_work")),

    # Thêm route logout (không đặt namespace app_work, gọi trực tiếp là 'logout')
    path('dang-nhap/', auth_views.LogoutView.as_view(next_page='app_customer:account'), name='logout'),

    path('HPexpress/', include('logistics.urls')),  # Tất cả route đổ về logistics/urls.py

    path('consult/', include('mentalConsult.urls', namespace='consult')),

    path('security/', include('app_security.urls', namespace='app_security')),

    path('mekong/', include('app_green.urls', namespace='app_green')),

    path('auth/', include('social_django.urls', namespace='social')),

    



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)