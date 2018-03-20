# _*_ coding: utf-8 _*_
__author__ = 'Bryce'
__date__ = '19/03/2018 12:13 PM'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredEdu(object):
    """用于判断用户是否登录，以便View类继承"""
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredEdu, self).dispatch(request, *args, **kwargs)