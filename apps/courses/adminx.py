# _*_ coding: utf-8 _*_
__author__ = 'Bryce'
__date__ = '12/03/2018 9:15 PM'

import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    """
    在xadmin后台中注册课程类字段
    """
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']
    readonly_fields = ['click_nums', 'fav_nums']
    exclude = ['fav_nums']
    style_fields = {"detail":"ueditor"}


class LessonAdmin(object):
    """
    在xadmin后台中注册课程类字段
    """
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name', 'add_time']
    # 指定连向Course表的外键course，要指定Course表的一个属性值才会在filter中显示
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    """
    在xadmin后台中注册视频类字段
    """
    list_display = ['name', 'lesson', 'add_time']
    search_fields = ['name', 'lesson', 'add_time']
    list_filter = ['name', 'lesson', 'add_time']


class CourseResourceAdmin(object):
    """
    在xadmin后台中注册课程资源类字段
    """
    list_display = ['name', 'course', 'add_time', 'download']
    search_fields = ['name', 'course', 'add_time', 'download']
    list_filter = ['name', 'course', 'add_time', 'download']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
