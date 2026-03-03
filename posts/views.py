# posts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.contrib import messages
from .models import Post, Like, Favorite
from .forms import PostForm

# 辅助函数：检查是否是管理员或拥有者
def is_staff_or_owner(user):
    return user.is_authenticated and (user.profile.role in ['mod', 'owner'] or user.is_superuser)

def home(request):
    return render(request, 'home.html')

def post_list(request):
    query = request.GET.get('q', '')
    posts = Post.objects.all()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    
    user_likes = []
    user_favs = []
    if request.user.is_authenticated:
        user_likes = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
        user_favs = Favorite.objects.filter(user=request.user).values_list('post_id', flat=True)

    return render(request, 'posts/list.html', {
        'posts': posts, 
        'query': query,
        'user_likes': user_likes,
        'user_favs': user_favs,
        'is_staff': is_staff_or_owner(request.user)
    })

@login_required
def post_create(request):
    # 检查是否被禁言
    if request.user.profile.is_muted:
        messages.error(request, "抱歉，你已被禁言，无法发布新帖。")
        return redirect('post_list')
        
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "发布成功！")
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 权限检查：只有作者本人、管理员或拥有者可以删除
    if request.user != post.author and not is_staff_or_owner(request.user):
        return HttpResponseForbidden("你没有权限删除此帖子")
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, "帖子已删除。")
    return redirect('post_list')

# ... (保留原有的 toggle_like, toggle_favorite, favorites_list, share_post 函数不变)
# ... 把它们放在这里 ...

@login_required
def toggle_like(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            post.likes_count -= 1
            liked = False
        else:
            post.likes_count += 1
            liked = True
        post.save()
        return JsonResponse({'count': post.likes_count, 'liked': liked})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def toggle_favorite(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        fav, created = Favorite.objects.get_or_create(user=request.user, post=post)
        if not created:
            fav.delete()
            post.favorites_count -= 1
            faved = False
        else:
            post.favorites_count += 1
            faved = True
        post.save()
        return JsonResponse({'count': post.favorites_count, 'favorited': faved})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).values_list('post', flat=True)
    posts = Post.objects.filter(id__in=favorites)
    return render(request, 'posts/favorites.html', {'posts': posts})

def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.shares_count += 1
    post.save()
    return redirect('post_list')

