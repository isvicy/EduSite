# _*_ coding: utf-8 _*_
__author__ = 'Bryce'
__date__ = '19/03/2018 12:07 PM'

import xadmin

from .models import UserAsk, CourseComments, UserMessage, UserCourse, UserFavorite


class UserAskAdmin(object):
    """在xadmin中注册首页用户咨询表"""
    list_display = ['name', 'mobile', 'add_time', 'course_name']
    search_fields = ['name', 'mobile', 'add_time', 'course_name']
    list_filter = ['name', 'mobile', 'add_time', 'course_name']


class CourseCommentsAdmin(object):
    """在xadmin中注册课程评论表"""
    list_display = ['user', 'course', 'add_time', 'comments']
    search_fields = ['user', 'course', 'add_time', 'comments']
    list_filter = ['user', 'course', 'add_time', 'comments']


class UserMessageAdmin(object):
    """在xadmin中注册用户消息表"""
    list_display = ['user', 'message', 'add_time', 'has_read']
    search_fields = ['user', 'message', 'add_time', 'has_read']
    list_filter = ['user', 'message', 'add_time', 'has_read']


class UserCourseAdmin(object):
    """在xadmin中注册用户课程表"""
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']


class UserFavoriteAdmin(object):
    """在xadmin中注册用户收藏表"""
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type', 'add_time']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
