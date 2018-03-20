# _*_ coding: utf-8 _*_
__author__ = 'Bryce'
__date__ = '19/03/2018 12:09 PM'

import re

from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    """ModelForm直接继承UserAsk表的部分字段，用于处理前端回传信息"""
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """对手机号作正则化验证"""
        mobile = self.cleaned_data['mobile']
        regex_mobile = "^(13[0-9]|14[579]|15[0-3,5-9]|17[0135678]|18[0-9])\\d{8}$"
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile number invalid")
