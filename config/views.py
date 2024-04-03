from django.shortcuts import render
from django.http import HttpResponse

from blog.views import CommonViewMixin
from django.views.generic import ListView
from .models import Link


class LinkView(CommonViewMixin, ListView):
    """友链视图"""
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    context_object_name = 'link_list'
    template_name = 'config/links.html'



