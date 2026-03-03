from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容 (支持文字和表情)")
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True, null=True, verbose_name="图片")
    link = models.URLField(blank=True, null=True, verbose_name="链接 (选填)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    likes_count = models.IntegerField(default=0)
    favorites_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'post')

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'post')

