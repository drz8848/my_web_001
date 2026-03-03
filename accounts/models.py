# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def __str__(self):
        return self.nickname or self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

