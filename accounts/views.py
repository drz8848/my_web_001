from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            user.profile.nickname = form.cleaned_data['nickname']
            user.profile.security_question = form.cleaned_data['security_question']
            user.profile.security_answer = form.cleaned_data['security_answer']
            user.profile.save()
            
            messages.success(request, "注册成功，请登录！")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        answer = request.POST.get('answer')
        new_pwd = request.POST.get('new_password')
        
        try:
            user = User.objects.get(username=username)
            if user.profile.security_answer.lower() == answer.lower():
                user.set_password(new_pwd)
                user.save()
                messages.success(request, "密码重置成功！请登录。")
                return redirect('login')
            else:
                messages.error(request, "密保答案错误")
        except User.DoesNotExist:
            messages.error(request, "用户不存在")
    
    # 如果是GET请求，先获取问题
    username_q = request.GET.get('username')
    question = ""
    if username_q:
        try:
            user = User.objects.get(username=username_q)
            question = user.profile.security_question
        except: pass
            
    return render(request, 'accounts/reset_password.html', {'question': question})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

