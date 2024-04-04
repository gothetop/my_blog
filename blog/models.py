from django.contrib.auth.models import User
from django.db import models
import mistune


class Category(models.Model):
    # 分类表
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "分类"

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        """返回导航分类"""
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for category in categories:
            if category.is_nav:
                nav_categories.append(category)
            else:
                normal_categories.append(category)
        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }


class Tag(models.Model):
    """标签类"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "标签"  # 设置了在管理页面的单数名称和复数名称都为标签

    def __str__(self):
        return self.name


class Post(models.Model):
    """文章表"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
        (STATUS_DRAFT, "草稿"),
    )

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")  # 该字段不希望由用户填写，而是在后台自动生成
    content = models.TextField(verbose_name="正文", help_text="正文必须为MarkDown格式")
    content_html = models.TextField(verbose_name="正文html格式", blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name="状态")
    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, verbose_name="标签", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ['-id']  # 根据id进行降序排列，新编写的文章在上面

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_tag(tag_id):
        """通过标签查询文章"""
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL) \
                .select_related('owner', 'category')
        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        """通过分类查询文章"""
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL) \
                .select_related('owner', 'category')
        return post_list, category

    @staticmethod
    def get_post_detail(post_id):
        """获取文章详情内容"""
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            post = None
        return post

    @classmethod
    def latest_posts(cls):
        """获取全部正常状态的文章"""
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL) \
            .select_related('owner', 'category')
        return queryset

    @classmethod
    def hot_posts(cls):
        """获取最热文章"""
        return cls.objects.filter(status=cls.STATUS_NORMAL).only('title', 'id').order_by('-pv')[:1]

    def save(self, *args, **kwargs):
        """重写保存方法，在content_html中默认添加数据"""
        self.content_html = mistune.markdown(self.content)
        # 这里就先默认是文章html格式的前140个字吧，后续再加逻辑处理
        self.desc = self.content_html[:140]

        super().save(*args, **kwargs)
