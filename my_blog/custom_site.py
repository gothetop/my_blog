from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    """自定义Site，继承自AdminSite"""
    site_header = '问心博客'
    site_title = "问心博客管理后台"
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')  # 这个name可以再通过reverse解耦时用到
