from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from django.contrib import messages
import os
from .models import Ouser

# Create your views here.

@login_required
def profile_view(request):
    return render(request, 'oauth/profile.html')

@login_required
def change_profile_view(request):
    if request.method == 'POST':
        old_avatar_file = request.user.avatar.path
        old_avatar_url = request.user.avatar.url
        # 上传文件需要使用request.FILES
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if not old_avatar_url == '/media/avatar/default.png':
                if os.path.exists(old_avatar_file):
                    os.remove(old_avatar_file)
            form.save()
            # 添加一条信息,表单验证成功就重定向到个人信息页面
            messages.add_message(request, messages.SUCCESS, '个人信息更新成功！')
            return redirect('oauth:profile')
    else:
        # 不是POST请求就返回空表单
        form = ProfileForm(instance=request.user)
    return render(request, 'oauth/change_profile.html', context={'form': form})



def create_user(request):
    """
    创建VIP内部用户
    :param request:
    :return:
    """
    user_name = ''                  #订单号
    password = user_name
    ticket = 2000       # 为用户设定默认的下载券数量
    new_user = Ouser(username=user_name, password=password, is_staff=True, avatar='avatar/staff.png', tickets=ticket)
    new_user.save()
    return


