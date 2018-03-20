# _*_ coding: utf-8 _*_
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord, Banner
from organization.models import CourseOrg, Teacher
from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.edu_utils import LoginRequiredEdu


class CustomBackend(ModelBackend):
    """
    重写authenticate函数，通过引入或的方法使得我们可以同时通过用户名和邮箱登录。
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except BaseException as e:
            return None


class IndexView(View):
    """首页View"""
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
            "all_banners": all_banners,
        })


class ActiveUserView(View):
    """用户激活View"""
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    """用户注册View"""
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_from': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get('password', "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()
            # 注册后发送欢迎信息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册Edusite"
            user_message.save()

            send_register_email(user_name, "register")

            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    """完成login逻辑"""
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未验证邮箱"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogOutView(View):
    """用户登出View"""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class ForgetPwdView(View):
    """忘记密码View"""
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)   #注意是request.POST,而不简单是request，这样传递进来的才是个列表。
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetView(View):
    """重置密码View"""
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    """修改密码View"""
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", '')
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", '')
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredEdu, View):
    """用户个人中心View"""
    def get(self, request):
        current = 'user_info'
        return render(request, 'usercenter-info.html', {"current": current})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class MyCourseView(LoginRequiredEdu, View):
    """用户课程View"""
    def get(self, request):
        current = 'user_course'
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses,
            "current": current
        })


class UserFavOrgView(LoginRequiredEdu, View):
    """用户收藏机构页View"""
    def get(self, request):
        current = 'user_fav'
        user_favs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        fav_org_ids = [user_fav.fav_id for user_fav in user_favs]
        user_fav_orgs = CourseOrg.objects.filter(id__in=fav_org_ids)
        return render(request, 'usercenter-fav-org.html', {
            "user_fav_orgs": user_fav_orgs,
            "current": current
        })


class UserFavTeacherView(LoginRequiredEdu, View):
    """用户收藏教师页View"""
    def get(self, request):
        user_favs = UserFavorite.objects.filter(user=request.user, fav_type=3)
        fav_teacher_ids = [user_fav.fav_id for user_fav in user_favs]
        user_fav_teachers = Teacher.objects.filter(id__in=fav_teacher_ids)
        return render(request, 'usercenter-fav-teacher.html', {
            "user_fav_teachers": user_fav_teachers
        })


class UserFavCourseView(LoginRequiredEdu, View):
    """用户收藏课程页View"""
    def get(self, request):
        user_favs = UserFavorite.objects.filter(user=request.user, fav_type=1)
        fav_course_ids = [user_fav.fav_id for user_fav in user_favs]
        user_fav_courses = Course.objects.filter(id__in=fav_course_ids)
        return render(request, 'usercenter-fav-course.html', {
            "user_fav_courses": user_fav_courses
        })


class MyMessageView(LoginRequiredEdu, View):
    """用户消息页View"""
    def get(self, request):
        current = 'user_message'
        all_message = UserMessage.objects.filter(user=request.user.id)
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for all_unread_message in all_unread_messages:
            all_unread_message.has_read = True
            all_unread_message.save()
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 3,  request=request)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            "all_message": messages,
            "current": current
        })


class UploadImageView(LoginRequiredEdu, View):
    """个人中心修改头像View"""
    def post(self, request):
        # ModelForm 实例化
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """个人中心修改密码View"""
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredEdu, View):
    """个人中心修改邮箱View"""
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredEdu, View):
    """修改个人邮箱"""
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            #然后删除对应的EmailVerified表中的信息
            existed_records.delete()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')



def page_not_found(request):
    """全局404设置"""
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    """全局500设置"""
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response