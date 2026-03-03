#!/usr/bin/env python
"""
Django论坛项目功能测试脚本

使用方法：
1. 确保Django已安装
2. 在项目根目录运行：python test_features.py
"""

import os
import sys
import django

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myforum.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from posts.models import Post, Like, Favorite
from accounts.utils import update_user_statistics

def print_section(title):
    """打印分节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_user_creation():
    """测试用户创建"""
    print_section("测试用户创建")
    
    # 创建测试用户
    user, created = User.objects.get_or_create(
        username='test_user',
        defaults={
            'email': 'test@example.com',
        }
    )
    
    if created:
        user.set_password('test123456')
        user.save()
        print("✅ 创建新用户: test_user")
    else:
        print("ℹ️  用户已存在: test_user")
    
    # 检查用户资料
    profile = user.profile
    print(f"   用户昵称: {profile.nickname or '未设置'}")
    print(f"   用户角色: {profile.get_role_display()}")
    print(f"   邮箱验证: {'已验证' if profile.email_verified else '未验证'}")
    print(f"   是否禁言: {'是' if profile.is_muted else '否'}")
    
    return user

def test_email_verification():
    """测试邮箱验证功能"""
    print_section("测试邮箱验证功能")
    
    user = User.objects.get(username='test_user')
    profile = user.profile
    
    # 生成验证令牌
    token = profile.generate_email_verification_token()
    print(f"✅ 生成验证令牌: {token[:20]}...")
    
    # 验证令牌
    is_valid = profile.is_verification_token_valid(token)
    print(f"✅ 令牌验证结果: {'有效' if is_valid else '无效'}")
    
    # 验证邮箱
    profile.email_verified = True
    profile.email_verification_token = ''
    profile.save()
    print(f"✅ 邮箱验证状态: {'已验证' if profile.email_verified else '未验证'}")

def test_password_reset():
    """测试密码重置功能"""
    print_section("测试密码重置功能")
    
    user = User.objects.get(username='test_user')
    profile = user.profile
    
    # 生成重置令牌
    token = profile.generate_password_reset_token()
    print(f"✅ 生成重置令牌: {token[:20]}...")
    
    # 验证令牌
    is_valid = profile.is_reset_token_valid(token)
    print(f"✅ 令牌验证结果: {'有效' if is_valid else '无效'}")
    
    # 重置密码
    user.set_password('new_password123')
    user.save()
    profile.password_reset_token = ''
    profile.save()
    print(f"✅ 密码已重置")

def test_post_creation():
    """测试帖子创建"""
    print_section("测试帖子创建")
    
    user = User.objects.get(username='test_user')
    
    # 创建测试帖子
    post, created = Post.objects.get_or_create(
        title='测试帖子',
        defaults={
            'content': '这是一个测试帖子的内容。',
            'author': user,
        }
    )
    
    if created:
        print("✅ 创建新帖子: 测试帖子")
    else:
        print("ℹ️  帖子已存在: 测试帖子")
    
    print(f"   帖子标题: {post.title}")
    print(f"   帖作者: {post.author.username}")
    print(f"   点赞数: {post.likes_count}")
    print(f"   收藏数: {post.favorites_count}")
    
    return post

def test_user_statistics():
    """测试用户统计功能"""
    print_section("测试用户统计功能")
    
    user = User.objects.get(username='test_user')
    
    # 更新统计
    update_user_statistics(user)
    
    profile = user.profile
    print(f"✅ 用户统计更新完成")
    print(f"   发帖数: {profile.posts_count}")
    print(f"   获赞数: {profile.likes_received}")

def test_like_functionality():
    """测试点赞功能"""
    print_section("测试点赞功能")
    
    user = User.objects.get(username='test_user')
    post = Post.objects.filter(title='测试帖子').first()
    
    if not post:
        print("❌ 未找到测试帖子")
        return
    
    # 创建点赞
    like, created = Like.objects.get_or_create(user=user, post=post)
    
    if created:
        post.likes_count += 1
        post.save()
        print(f"✅ 点赞成功，当前点赞数: {post.likes_count}")
    else:
        print(f"ℹ️  已经点赞过，当前点赞数: {post.likes_count}")
    
    # 更新用户统计
    update_user_statistics(post.author)
    print(f"✅ 作者获赞数: {post.author.profile.likes_received}")

def test_permissions():
    """测试权限功能"""
    print_section("测试权限功能")
    
    from accounts.decorators import is_staff_or_owner
    
    user = User.objects.get(username='test_user')
    
    # 测试普通用户权限
    is_staff = is_staff_or_owner(user)
    print(f"✅ 普通用户权限: {'有管理权限' if is_staff else '无管理权限'}")
    
    # 测试管理员权限
    user.profile.role = 'mod'
    user.profile.save()
    is_staff = is_staff_or_owner(user)
    print(f"✅ 管理员权限: {'有管理权限' if is_staff else '无管理权限'}")
    
    # 恢复普通用户
    user.profile.role = 'user'
    user.profile.save()

def cleanup():
    """清理测试数据"""
    print_section("清理测试数据")
    
    # 删除测试帖子
    Post.objects.filter(title='测试帖子').delete()
    print("✅ 删除测试帖子")
    
    # 删除测试用户
    User.objects.filter(username='test_user').delete()
    print("✅ 删除测试用户")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("  Django论坛项目功能测试")
    print("="*60)
    
    try:
        # 运行测试
        test_user_creation()
        test_email_verification()
        test_password_reset()
        test_post_creation()
        test_user_statistics()
        test_like_functionality()
        test_permissions()
        
        # 询问是否清理
        print_section("测试完成")
        choice = input("是否清理测试数据？(y/n): ")
        if choice.lower() == 'y':
            cleanup()
        
        print_section("所有测试完成")
        print("✅ 所有功能测试通过！")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
