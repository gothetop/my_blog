from django.shortcuts import render
from django.http import HttpResponse


def links(request):
    """友链视图"""
    return HttpResponse("links")

