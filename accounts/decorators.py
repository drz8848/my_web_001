# accounts/decorators.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

def email_verified_required(view_func):
    """要求邮箱已验证的装饰器"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # 如果邮箱未验证且强制要求验证
        if not request.user.profile.email_verified:
            messages.warning(request, "请先验证您的邮箱地址")
            return redirect('profile')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def role_required(*roles):
    """要求特定角色的装饰器"""
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.profile.role not in roles and not request.user.is_superuser:
                messages.error(request, "您没有权限访问此页面")
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def not_muted_required(view_func):
    """要求未被禁言的装饰器"""
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.profile.is_muted:
            messages.error(request, "您已被禁言，无法执行此操作")
            return redirect('profile')
        return view_func(request, *args, **kwargs)
    return wrapper

def is_staff_or_owner(user):
    """检查用户是否为管理员或拥有者"""
    return user.is_authenticated and (user.profile.role in ['mod', 'owner'] or user.is_superuser)
