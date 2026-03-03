from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.http import Http404

from .models import UserProfile
from .forms import RegisterForm, ProfileEditForm, PasswordResetRequestForm, PasswordResetConfirmForm
from .utils import send_verification_email, send_password_reset_email, update_user_statistics
from .decorators import not_muted_required

def register(request):
    """用户注册"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = True  # 默认激活，后续可根据配置要求邮箱验证
            user.save()
            
            # 保存用户资料
            user.profile.nickname = form.cleaned_data['nickname']
            user.profile.security_question = form.cleaned_data['security_question']
            user.profile.security_answer = form.cleaned_data['security_answer']
            user.profile.save()
            
            # 发送验证邮件
            if send_verification_email(request, user):
                messages.success(request, "注册成功！验证邮件已发送至您的邮箱，请查收。")
            else:
                messages.warning(request, "注册成功，但验证邮件发送失败，请稍后在个人中心重新发送。")
            
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_email(request, token):
    """验证邮箱"""
    try:
        # 查找具有该令牌的用户
        profile = UserProfile.objects.get(email_verification_token=token)
        
        if profile.is_verification_token_valid(token, settings.EMAIL_VERIFICATION_EXPIRE_HOURS):
            profile.email_verified = True
            profile.email_verification_token = ''
            profile.email_verification_sent_at = None
            profile.save()
            messages.success(request, "邮箱验证成功！")
        else:
            messages.error(request, "验证链接已失效或无效，请重新发送验证邮件。")
            
    except UserProfile.DoesNotExist:
        messages.error(request, "无效的验证链接。")
    
    return redirect('login')

@login_required
def resend_verification_email(request):
    """重新发送验证邮件"""
    if request.user.profile.email_verified:
        messages.info(request, "您的邮箱已经验证过了。")
    else:
        if send_verification_email(request, request.user):
            messages.success(request, "验证邮件已重新发送，请查收。")
        else:
            messages.error(request, "验证邮件发送失败，请稍后重试。")
    
    return redirect('profile')

@login_required
def profile(request):
    """个人中心"""
    # 更新用户统计数据
    update_user_statistics(request.user)
    
    # 获取用户的帖子
    user_posts = request.user.posts.all().order_by('-created_at')[:5]
    
    context = {
        'user_posts': user_posts,
        'email_verification_required': settings.EMAIL_VERIFICATION_REQUIRED,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_edit(request):
    """编辑个人资料"""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            
            # 更新个人资料
            user.profile.nickname = form.cleaned_data['nickname']
            user.profile.security_question = form.cleaned_data['security_question']
            user.profile.security_answer = form.cleaned_data['security_answer']
            
            # 如果邮箱改变了，需要重新验证
            if user.email != request.user.email:
                user.profile.email_verified = False
                messages.info(request, "邮箱地址已更改，请重新验证。")
            
            user.save()
            user.profile.save()
            
            messages.success(request, "个人资料更新成功！")
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
        # 预填充个人资料字段
        form.fields['nickname'].initial = request.user.profile.nickname
        form.fields['security_question'].initial = request.user.profile.security_question
        form.fields['security_answer'].initial = request.user.profile.security_answer
    
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def change_password(request):
    """修改密码"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "密码修改成功！请重新登录。")
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})

def password_reset_request(request):
    """密码重置请求"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                if send_password_reset_email(request, user):
                    messages.success(request, "密码重置邮件已发送至您的邮箱，请查收。")
                else:
                    messages.error(request, "邮件发送失败，请稍后重试。")
            except User.DoesNotExist:
                # 为了安全，不透露邮箱是否存在
                messages.success(request, "如果该邮箱已注册，您将收到密码重置邮件。")
            
            return redirect('login')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'accounts/password_reset_request.html', {'form': form})

def reset_password_confirm(request, token):
    """确认密码重置"""
    try:
        profile = UserProfile.objects.get(password_reset_token=token)
        
        if not profile.is_reset_token_valid(token, settings.PASSWORD_RESET_EXPIRE_HOURS):
            messages.error(request, "重置链接已失效或无效。")
            return redirect('password_reset_request')
        
        if request.method == 'POST':
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                user = profile.user
                user.set_password(form.cleaned_data['password'])
                user.save()
                
                # 清除重置令牌
                profile.password_reset_token = ''
                profile.password_reset_sent_at = None
                profile.save()
                
                messages.success(request, "密码重置成功！请使用新密码登录。")
                return redirect('login')
        else:
            form = PasswordResetConfirmForm()
        
        return render(request, 'accounts/reset_password_confirm.html', {'form': form})
        
    except UserProfile.DoesNotExist:
        messages.error(request, "无效的重置链接。")
        return redirect('password_reset_request')

def reset_password(request):
    """旧的密保问题密码重置（保留兼容性）"""
    if request.method == 'POST':
        username = request.POST.get('username')
        answer = request.POST.get('answer')
        new_pwd = request.POST.get('new_password')
        
        try:
            user = User.objects.get(username=username)
            if user.profile.security_answer and user.profile.security_answer.lower() == answer.lower():
                user.set_password(new_pwd)
                user.save()
                messages.success(request, "密码重置成功！请登录。")
                return redirect('login')
            else:
                messages.error(request, "密保答案错误")
        except User.DoesNotExist:
            messages.error(request, "用户不存在")
    
    # 如果是GET请求，先获取问题
    username_q = request.GET.get('username')
    question = ""
    if username_q:
        try:
            user = User.objects.get(username=username_q)
            question = user.profile.security_question or "未设置密保问题"
        except: pass
            
    return render(request, 'accounts/reset_password.html', {'question': question})
