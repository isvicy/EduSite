# _*_ coding: utf-8 _*_
__author__ = 'Bryce'
__date__ = '19/03/2018 12:06 PM'

from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView

app_name = 'courses'  # 在Django2.0中，如果在主app下使用namespace参数，那么就需要在从app下设置app_name字段
urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),
    # 添加课程评论
    url(r'^add_comment/$', AddCommentView.as_view(), name="add_comment")

]
