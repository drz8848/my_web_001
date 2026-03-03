# Generated migration for email verification and user statistics

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_is_muted_userprofile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_verified',
            field=models.BooleanField(default=False, verbose_name='邮箱是否已验证'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email_verification_token',
            field=models.CharField(blank=True, max_length=64, verbose_name='邮箱验证令牌'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email_verification_sent_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='验证邮件发送时间'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='password_reset_token',
            field=models.CharField(blank=True, max_length=64, verbose_name='密码重置令牌'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='password_reset_sent_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='重置邮件发送时间'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='posts_count',
            field=models.IntegerField(default=0, verbose_name='发帖数量'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='likes_received',
            field=models.IntegerField(default=0, verbose_name='获得的点赞数'),
        ),
    ]
