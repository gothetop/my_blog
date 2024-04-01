from django.shortcuts import render
from django.http import HttpResponse

from blog.models import Tag, Post, Category
from config.models import SideBar


def post_list(request, category_id=None, tag_id=None):
    """文章列表视图"""
    category = None
    tag = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()
    context = {
        'tag': tag,
        'category': category,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context)


def post_detail(request, post_id):
    """文章详情视图"""
    post = Post.get_post_detail(post_id)
    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, "blog/detail.html", context)
