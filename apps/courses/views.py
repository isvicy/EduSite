# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from operation.models import UserFavorite
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, CourseResource
from operation.models import CourseComments, UserCourse
from utils.edu_utils import LoginRequiredEdu


class CourseListView(View):
    """课程列表View"""
    def get(self, request):
        current = 'courses_list'
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)
                                             |Q(detail__icontains=search_keywords))
        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 设置分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            "sort": sort,
            "hot_courses": hot_courses,
            "current": current,
        })


class CourseDetailView(View):
    """课程详情页View"""
    def get(self, request, course_id):
        course_info = Course.objects.get(id=int(course_id))   # 需要注意filter和get方法的异同
        course_info.click_nums += 1  # 进入详情页，则课程点击数加一
        course_info.save()

        # 用户收藏的显示
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course_info.course_org.id, fav_type=2):
                has_fav_org = True

        # 相关课程显示
        tag = course_info.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request, "course-detail.html", {
            'course_info': course_info,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class CourseInfoView(LoginRequiredEdu, View):
    """课程介绍页View"""
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        all_resources = CourseResource.objects.filter(course=course)
        # 取得学过该课程的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 取得用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        #取得上述用户学习的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:4]

        return render(request, "course-video.html", {
            "course": course,
            "all_resource": all_resources,
            "related_courses": courses

        })


class CourseCommentView(LoginRequiredEdu, View):
    """课程评论页View"""
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.filter(course=course).all()
        all_resources = CourseResource.objects.filter(course=course).all()
        # 取得学过该课程的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 取得用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取得上述用户学习的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        # 设置分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_comments, 10, request=request)
        user_comment = p.page(page)

        return render(request, "course-comment.html", {
            "course": course,
            "all_comments": user_comment,
            "all_resources": all_resources,
            "related_courses": courses
        })


class AddCommentView(View):
    """ajax处理用户添加评论的行为，和用户收藏功能类似"""
    def post(self, request):
        if not request.user.is_authenticated:
            # 判断用户登陆状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')
