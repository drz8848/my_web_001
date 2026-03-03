from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="密码")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="确认密码")
    nickname = forms.CharField(max_length=50, label="昵称")
    security_question = forms.CharField(max_length=200, label="密保问题 (例如：我的宠物叫什么？)")
    security_answer = forms.CharField(max_length=200, label="密保答案")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirm']:
            raise forms.ValidationError("两次密码输入不一致")
        return cd['password_confirm']

