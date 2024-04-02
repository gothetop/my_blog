from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from blog.models import Tag, Post, Category
from config.models import SideBar

"""
# 函数视图如下：
def post_list(request, category_id=None, tag_id=None):
    # 文章列表视图
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
    # 文章详情页
    post = Post.get_post_detail(post_id)
    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, "blog/detail.html", context)
"""


class CommonViewMixin:
    """通用类：评论，上下导航栏"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


# 类视图如下
class IndexView(CommonViewMixin, ListView):
    """首页类视图"""
    queryset = Post.latest_posts()
    paginate_by = 5  # 一页展示五条数据
    context_object_name = "post_list"  # 修改在模板中的对象名
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    """分类页面视图，继承自首页"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')  # 在url请求链接中找到category_id参数
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """重写页面获取到的数据集, 根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')   # self.kwargs指的是url的请求链接中带来的东西
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    """标签页，继承于首页类视图"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """重写数据集，根据标签进行筛选"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    """文章详情页，继承通用类和DetailView类"""
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = "post"
    pk_url_kwarg = 'post_id'
