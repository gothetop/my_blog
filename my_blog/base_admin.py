"""管理后台基类"""
from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    继承自ModelAdmin
    1.用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
    2.用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner', )

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     """重写外键查询获得的数据集"""
    #     # 这样每个用户在创建文章的时候就只能看到自己设置的标签或者分类了
    #     if db_field.name == 'category':
    #         kwargs['queryset'] = Category.objects.filter(owner=request.user)
    #     elif db_field.name == 'tag':
    #         kwargs['queryset'] = Tag.objects.filter(owner=request.user)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
    #
    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == 'category':
    #         kwargs['queryset'] = Tag.objects.filter(owner=request.user)
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)



