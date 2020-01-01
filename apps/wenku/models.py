from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone
from oauth.models import Ouser


class DownloadDetails(models.Model):
    """
    下载详情，使用username 与用户表关联
    """
    username = models.CharField(verbose_name='用户名', max_length=15)
    title = models.TextField(verbose_name='文件名称', max_length=150)
    download_url = models.TextField(verbose_name='下载网址', max_length=300)
    download_time = models.DateTimeField(verbose_name='下载时间', default=timezone.now)
    del_token = models.IntegerField(verbose_name='下载所需券数')
    downloaders = models.ForeignKey(Ouser, verbose_name='下载详情',
                                    default='', related_name='user_downloaders', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['-download_time']

    def __str__(self):
        return self.title[:20]
