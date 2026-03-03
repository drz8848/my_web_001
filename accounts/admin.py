# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# 定义内联 Admin，让用户资料显示在用户编辑页
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户权限与资料'
    readonly_fields = ('email_verified_display',)

    def email_verified_display(self, obj):
        return "已验证" if obj.email_verified else "未验证"
    email_verified_display.short_description = '邮箱验证状态'

# 定义新的 User Admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    
    # 只有网站拥有者（超级用户）可以编辑用户的角色
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['is_superuser'] # 管理员不能把自己设为超级用户
        return super().get_readonly_fields(request, obj)
    
    # 控制列表显示
    list_display = ('username', 'email', 'nickname_display', 'role_display', 'email_verified_display', 
                   'is_muted_display', 'posts_count_display', 'likes_received_display', 'is_staff', 'date_joined')
    list_filter = ('profile__role', 'profile__is_muted', 'profile__email_verified', 'is_staff')
    search_fields = ('username', 'email', 'profile__nickname')
    
    def nickname_display(self, obj):
        return obj.profile.nickname or '-'
    nickname_display.short_description = '昵称'
    
    def role_display(self, obj):
        return obj.profile.get_role_display()
    role_display.short_description = '角色'
    
    def email_verified_display(self, obj):
        return obj.profile.email_verified
    email_verified_display.short_description = '邮箱验证'
    email_verified_display.boolean = True
    
    def is_muted_display(self, obj):
        return obj.profile.is_muted
    is_muted_display.boolean = True
    is_muted_display.short_description = '是否禁言'
    
    def posts_count_display(self, obj):
        return obj.profile.posts_count
    posts_count_display.short_description = '发帖数'
    
    def likes_received_display(self, obj):
        return obj.profile.likes_received
    likes_received_display.short_description = '获赞数'

# 重新注册 User Admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
