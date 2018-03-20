# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg, Teacher


class Course(models.Model):
    """课程类，包含课程相关信息"""
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=20, verbose_name=u"课程描述")
    category = models.CharField(max_length=300, verbose_name=u"课程类别", default=u"后端开发")
    # 将课程详情设置为富文本
    detail = UEditorField(verbose_name=u'课程详情	', width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")
    degree = models.CharField(choices=(("cj", u"初级"), ("zj", "中级"), ("gj", "高级")), max_length=2, verbose_name=u"难度")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=u"课程老师", null=True, blank=True)
    youneed_know = models.CharField(max_length=300, verbose_name=u"课程须知", default="")
    teacher_tell = models.CharField(max_length=300, verbose_name=u"老师能告诉你什么", default="")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    tag = models.CharField(default="", verbose_name=u"课程标签", max_length=10)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_lesson_nums(self):
        """获取章节信息数"""
        return self.lesson_set.all().count()

    def get_learn_users(self):
        """获取课程的学习用户"""
        learn_users = self.usercourse_set.all()
        return learn_users

    def get_course_lesson(self):
        """获取章节信息"""
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """章节信息类"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程章节"
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        """获取章节对应视频"""
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    """章节视频类"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    url = models.CharField(max_length=200, default='', verbose_name=u'访问地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    """课程资源类"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
