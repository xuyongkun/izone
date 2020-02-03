from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import DownloadDetails
from django.views.decorators.http import require_POST
from django.http import HttpResponse

import json
from wenku.loginbaidu import LoginBaidu


headers = {
    "Host": "passport.baidu.com",
    "Referer": "https://www.baidu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
}

@login_required
def download_details_view(request):
    """
    显示下载详情
    :param request:
    :return:
    """
    return render(request, 'wenku/index.html')

def Wenku_view(request):
    """
    文库下载主页
    :param request:
    :return:
    """
    return render(request, 'wenku/index.html')

@login_required
@require_POST
def download_document(request):
    """
    下载文档
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = request.POST
        user = request.user                 # 获取用户名
        doc_url = data.get('document_url')  # 获取用户输入的要下载的URL
        browser_type = data.get('browser_type')     #获取浏览器的类型
        # 判断URL 是否是百度文库
        url_pre = 'https://wenku.baidu.com'
        if doc_url.startswith(url_pre):
            # 是文库网址，首先登录百度
            login_baidu = LoginBaidu()
            # 取得登陆绘画（session）
            session = login_baidu.get_session()
            # 获取文档正式url
            init_url = login_baidu.download_document(session, doc_url)
            # session.get(doc_url, headers=headers, verify=False)
            data = {'msg': 'success', 'url': init_url}
            return HttpResponse(json.dumps(data), content_type='text/html;charset=utf-8')
        else:
            data = {'msg': 'not baidu'}
            return HttpResponse(json.dumps(data), content_type='text/html;charset=utf-8')




class IndexView(generic.ListView):
    model = DownloadDetails
    template_name = 'wenku/index.html'
    context_object_name = 'wenku'



