from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="密码",
        min_length=6
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="确认密码"
    )
    nickname = forms.CharField(
        max_length=50, 
        label="昵称",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    security_question = forms.CharField(
        max_length=200, 
        label="密保问题 (例如：我的宠物叫什么？)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    security_answer = forms.CharField(
        max_length=200, 
        label="密保答案",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirm']:
            raise forms.ValidationError("两次密码输入不一致")
        return cd['password_confirm']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("该邮箱已被注册")
        return email

class ProfileEditForm(forms.ModelForm):
    """个人资料编辑表单"""
    nickname = forms.CharField(
        max_length=50, 
        label="昵称",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    security_question = forms.CharField(
        max_length=200, 
        label="密保问题",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    security_answer = forms.CharField(
        max_length=200, 
        label="密保答案",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # 检查邮箱是否被其他用户使用
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("该邮箱已被其他用户使用")
        return email

class PasswordResetRequestForm(forms.Form):
    """密码重置请求表单"""
    email = forms.EmailField(
        label="邮箱地址",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入注册时使用的邮箱'})
    )

class PasswordResetConfirmForm(forms.Form):
    """密码重置确认表单"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="新密码",
        min_length=6
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="确认新密码"
    )
    
    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirm']:
            raise forms.ValidationError("两次密码输入不一致")
        return cd['password_confirm']
