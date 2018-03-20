# _*_ coding: utf-8 _*_
__author__ = 'Bryce'
__date__ = '19/03/2018 12:08 PM'

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    """在xadmin中注册城市表"""
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc', 'add_time']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    """在xadmin中注册课程机构表"""
    list_display = ['name', 'desc', 'add_time', 'click_nums', 'fav_nums', 'address', 'city']
    search_fields = ['name', 'desc', 'add_time', 'click_nums', 'fav_nums', 'address', 'city']
    list_filter = ['name', 'desc', 'add_time', 'click_nums', 'fav_nums', 'address', 'city']


class TeacherAdmin(object):
    """在xadmin中注册教师表"""
    list_display = ['name', 'org', 'click_nums', 'fav_nums', 'work_years', 'work_company', 'work_position', 'points']
    search_fields = ['name', 'org', 'click_nums', 'fav_nums', 'work_years', 'work_company', 'work_position', 'points']
    list_filter = ['name', 'org', 'click_nums', 'fav_nums', 'work_years', 'work_company', 'work_position', 'points']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
