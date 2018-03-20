# _*_ coding: utf-8 _*_
__author__ = 'Bryce'
__date__ = '19/03/2018 12:11 PM'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner, UserProfile


class BaseSetting(object):
    """开启xadmin主题设置"""
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    """xadmin后台的一些全局设置"""
    site_title = "EduDemo 后台管理系统"
    site_footer = "EduDemo"
    menu_style = "accordion"  # 列表折叠


class EmailVerifyRecordAdmin(object):
    """在xadmin中注册邮箱验证码表"""
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    """在xadmin中注册轮播图表"""
    list_display = ["title", "image", "url", "index", "add_time"]
    search_fields = ["title", "image", "url", "index", "add_time"]
    list_filter = ["title", "url", "index", "add_time"]


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)