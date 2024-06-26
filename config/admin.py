from django.contrib import admin

from config.models import SideBar, Link
from my_blog.custom_site import custom_site
from my_blog.base_admin import BaseOwnerAdmin


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = (
        'title', 'href', 'status',
        'weight', 'created_time',
    )
    fields = (
        'title', 'href', 'status', 'weight'
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = (
        'title', 'display_type',
        'content', 'created_time',
    )
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)


