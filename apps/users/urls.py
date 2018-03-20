# _*_ coding: utf-8 _*_
__author__ = 'Bryce'
__date__ = '19/03/2018 12:13 PM'

from django.conf.urls import url

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView
from .views import UserFavOrgView, UserFavTeacherView, UserFavCourseView, MyMessageView


app_name = 'users'
urlpatterns = [
    # 用户个人中心
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 用户相关
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
    url(r'^myfav/org/$', UserFavOrgView.as_view(), name='myfav_org'),
    url(r'^myfav/teacher/$', UserFavTeacherView.as_view(), name='myfav_teacher'),
    url(r'^myfav/course/$', UserFavCourseView.as_view(), name='myfav_course'),
    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

]