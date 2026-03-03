# posts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('new/', views.post_create, name='post_create'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'), # 新增
    path('like/<int:pk>/', views.toggle_like, name='toggle_like'),
    path('favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('share/<int:pk>/', views.share_post, name='share_post'),
    path('my-favorites/', views.favorites_list, name='favorites'),
]

