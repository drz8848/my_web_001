# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import secrets

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('user', '普通用户'),
        ('mod', '管理员'),
        ('owner', '网站拥有者'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, verbose_name="昵称", blank=True)
    security_question = models.CharField(max_length=200, verbose_name="密保问题", blank=True)
    security_answer = models.CharField(max_length=200, verbose_name="密保答案", blank=True)
    
    # 新增字段
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name="用户角色")
    is_muted = models.BooleanField(default=False, verbose_name="是否被禁言")
    
    # 邮箱验证相关字段
    email_verified = models.BooleanField(default=False, verbose_name="邮箱是否已验证")
    email_verification_token = models.CharField(max_length=64, blank=True, verbose_name="邮箱验证令牌")
    email_verification_sent_at = models.DateTimeField(null=True, blank=True, verbose_name="验证邮件发送时间")
    
    # 密码重置相关字段
    password_reset_token = models.CharField(max_length=64, blank=True, verbose_name="密码重置令牌")
    password_reset_sent_at = models.DateTimeField(null=True, blank=True, verbose_name="重置邮件发送时间")
    
    # 用户统计
    posts_count = models.IntegerField(default=0, verbose_name="发帖数量")
    likes_received = models.IntegerField(default=0, verbose_name="获得的点赞数")
    
    def __str__(self):
        return self.nickname or self.user.username
    
    def generate_email_verification_token(self):
        """生成邮箱验证令牌"""
        self.email_verification_token = secrets.token_urlsafe(32)
        self.email_verification_sent_at = timezone.now()
        self.save()
        return self.email_verification_token
    
    def generate_password_reset_token(self):
        """生成密码重置令牌"""
        self.password_reset_token = secrets.token_urlsafe(32)
        self.password_reset_sent_at = timezone.now()
        self.save()
        return self.password_reset_token
    
    def is_verification_token_valid(self, token, expire_hours=24):
        """检查验证令牌是否有效"""
        if not self.email_verification_token or self.email_verification_token != token:
            return False
        if not self.email_verification_sent_at:
            return False
        expire_time = self.email_verification_sent_at + timezone.timedelta(hours=expire_hours)
        return timezone.now() < expire_time
    
    def is_reset_token_valid(self, token, expire_hours=1):
        """检查重置令牌是否有效"""
        if not self.password_reset_token or self.password_reset_token != token:
            return False
        if not self.password_reset_sent_at:
            return False
        expire_time = self.password_reset_sent_at + timezone.timedelta(hours=expire_hours)
        return timezone.now() < expire_time

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
