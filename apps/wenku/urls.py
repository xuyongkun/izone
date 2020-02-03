#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
"""
@File           :   urls.py 
@Contact        :   xuyongkun22@163.com
@Modify Time    :   2019/4/19 23:17 
@Author         :   kenny
@Version        :   1.0
@Desciption     :   None
@License        :   (C)Copyright 2017-2019, kenny 
"""
from django.conf.urls import url
from django.urls import path
from .views import download_details_view, download_document, Wenku_view


app_name = 'wenku'

urlpatterns = [
    path('', Wenku_view, name='wenku_index'),                       # 文库下载主页
    path('', download_details_view, name='download_detail'),         # 显示用户下载信息
    path('download', download_document, name='download_document'),            # 下载文档
]