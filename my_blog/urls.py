"""
URL configuration for my_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from .custom_site import custom_site
from blog.views import post_list, post_detail
from config.views import links

urlpatterns = [
    path('super_admin/', admin.site.urls),   # 超级管理员后台
    path('admin/', custom_site.urls),   # 博客内容管理后台
    path('', post_list, name='index'),
    path('category/<int:category_id>/', post_list, name='category-list'),
    path('tag/<int:tag_id>/', post_list, name='tag-list'),
    path('post/<int:post_id>/', post_detail, name='post-detail'),
    path('links/', links, name='links'),
]
