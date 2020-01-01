from django.contrib import admin
from .models import DownloadDetails

# Register your models here.

@admin.register(DownloadDetails)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ('username', 'title', 'download_url', 'download_time', 'del_token')


    def get_queryset(self, request):
        qs = super(DownloadAdmin, self).get_queryset(request)
        return qs.filter(author=request.user)