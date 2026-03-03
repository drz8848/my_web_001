# accounts/utils.py
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import logging

logger = logging.getLogger(__name__)

def send_verification_email(request, user):
    """发送邮箱验证邮件"""
    try:
        # 生成验证令牌
        token = user.profile.generate_email_verification_token()
        
        # 构建验证链接
        verify_url = request.build_absolute_uri(
            reverse('verify_email', kwargs={'token': token})
        )
        
        subject = f'{settings.EMAIL_SUBJECT_PREFIX}请验证您的邮箱地址'
        message = f'''
亲爱的 {user.profile.nickname or user.username}：

感谢您注册东方幻绮梦！

请点击以下链接验证您的邮箱地址：
{verify_url}

此链接将在 {settings.EMAIL_VERIFICATION_EXPIRE_HOURS} 小时后失效。

如果您没有注册此账号，请忽略此邮件。

祝好，
东方幻绮梦团队
'''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        logger.info(f"验证邮件已发送至 {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"发送验证邮件失败: {str(e)}")
        return False

def send_password_reset_email(request, user):
    """发送密码重置邮件"""
    try:
        # 生成重置令牌
        token = user.profile.generate_password_reset_token()
        
        # 构建重置链接
        reset_url = request.build_absolute_uri(
            reverse('reset_password_confirm', kwargs={'token': token})
        )
        
        subject = f'{settings.EMAIL_SUBJECT_PREFIX}重置您的密码'
        message = f'''
亲爱的 {user.profile.nickname or user.username}：

我们收到了您的密码重置请求。

请点击以下链接重置您的密码：
{reset_url}

此链接将在 {settings.PASSWORD_RESET_EXPIRE_HOURS} 小时后失效。

如果您没有请求重置密码，请忽略此邮件，您的密码不会被更改。

祝好，
东方幻绮梦团队
'''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        logger.info(f"密码重置邮件已发送至 {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"发送密码重置邮件失败: {str(e)}")
        return False

def update_user_statistics(user):
    """更新用户统计数据"""
    from posts.models import Post, Like
    
    # 更新发帖数
    user.profile.posts_count = user.posts.count()
    
    # 更新获得的点赞数
    user_posts = user.posts.all()
    likes_received = Like.objects.filter(post__in=user_posts).count()
    user.profile.likes_received = likes_received
    
    user.profile.save()
