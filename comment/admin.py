from django.contrib import admin

from comment.models import Comment
from my_blog.custom_site import custom_site
from my_blog.base_admin import BaseOwnerAdmin


@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')

